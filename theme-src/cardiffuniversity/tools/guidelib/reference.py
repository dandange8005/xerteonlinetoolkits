"""Data for the reference pages: colours, other design tokens, utility classes and legacy classes.

Colours and tokens are read from tokens/tokens.json, so the pages cannot drift from the theme.
guide/reference.toml gives each token group an author-facing title and intro; a token group with
no entry is a ReferenceDataError, so a new group cannot be left off the pages by accident.
"""
import json
import math
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALIAS = re.compile(r"^\{(cu-[\w-]+)\}$")
SLUG = re.compile(r"^[a-z0-9-]+$")
AA_TEXT = 4.5  # WCAG AA contrast for body text
WHITE_TOKEN, INK_TOKEN = "cu-white", "cu-black"


class ReferenceDataError(ValueError):
    def __init__(self, source, message):
        super().__init__(f"{source}: {message}")


@dataclass(frozen=True)
class Token:
    name: str  # as in tokens.json, so without the leading --
    value: str  # as written
    resolved: str  # the value with any alias followed
    alias_of: str | None
    note: str


@dataclass(frozen=True)
class Group:
    id: str
    title: str
    intro: str
    tokens: tuple


@dataclass(frozen=True)
class Reference:
    palette: tuple  # groups whose tokens are all colours
    tokens: tuple  # every other group
    utilities: tuple  # (heading, guidance, ((class, value), ...))
    legacy: tuple  # ((class, reason), ...)
    white: str
    ink: str


def luminance(colour):
    """Relative luminance of a #RRGGBB colour (WCAG 2)."""
    channels = []
    for start in (1, 3, 5):
        value = int(colour[start:start + 2], 16) / 255
        channels.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first, second):
    """Contrast ratio between two colours. It is the same whichever one is the text."""
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def ratio_text(ratio):
    """The ratio rounded down, so a ratio just under a threshold never reads as passing it."""
    return f"{math.floor(ratio * 10) / 10:.1f}:1"


def passes_aa(ratio):
    return ratio >= AA_TEXT


def _natural(name):
    """A sort key that puts m-2 before m-10."""
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", name)]


def _resolve(name, table, source, seen=()):
    """The value of a token with any alias followed, and the name it is an alias of (or None)."""
    value = table[name]
    match = ALIAS.match(value)
    if not match:
        return value, None
    target = match.group(1)
    if target == name or target in seen:
        raise ReferenceDataError(source, f"token {name} is part of an alias loop")
    if target not in table:
        raise ReferenceDataError(source, f"token {name} refers to {{{target}}}, which does not exist")
    return _resolve(target, table, source, seen + (name,))[0], target


def _read_copy(path):
    try:
        data = tomllib.loads(Path(path).read_text(encoding="utf-8-sig"))
    except OSError as error:
        raise ReferenceDataError(path, f"cannot read ({error})") from None
    except UnicodeDecodeError:
        raise ReferenceDataError(path, "is not saved as UTF-8") from None
    except tomllib.TOMLDecodeError as error:
        raise ReferenceDataError(path, f"not valid TOML ({error})") from None
    entries = data.get("groups")
    if not isinstance(entries, list) or not entries:
        raise ReferenceDataError(path, "needs at least one [[groups]] entry")
    out, seen = [], set()
    for number, entry in enumerate(entries, 1):
        where = f"[[groups]] entry {number}"
        if not isinstance(entry, dict):
            raise ReferenceDataError(path, f"{where} must be a table")
        extra = sorted(set(entry) - {"id", "title", "intro"})
        if extra:
            raise ReferenceDataError(path, f"{where}: unknown key(s): {', '.join(extra)}")
        for key in ("id", "title", "intro"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ReferenceDataError(path, f"{where}: missing '{key}'")
        if not SLUG.match(entry["id"]):
            raise ReferenceDataError(path, f"{where}: id must use only a-z, 0-9 and hyphens")
        if entry["id"] in seen:
            raise ReferenceDataError(path, f"group '{entry['id']}' is listed twice")
        seen.add(entry["id"])
        out.append(entry)
    return out


def load_reference(tokens_path, copy_path, utilities, legacy):
    """Everything the reference pages show. utilities and legacy come from tools/theme_css.py."""
    tokens_path, copy_path = Path(tokens_path), Path(copy_path)
    try:
        data = json.loads(tokens_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReferenceDataError(tokens_path, f"cannot read the tokens ({error})") from None
    groups = {key: value for key, value in data.items() if not key.startswith("$")}
    table = {name: token["$value"] for group in groups.values() for name, token in group.items()
             if not name.startswith("$")}
    for needed in (WHITE_TOKEN, INK_TOKEN):
        if needed not in table:
            raise ReferenceDataError(tokens_path, f"the reference pages need a {needed} token")
    entries = _read_copy(copy_path)
    described = [entry["id"] for entry in entries]
    missing = [key for key in groups if key not in described]
    if missing:
        raise ReferenceDataError(copy_path, f"no entry for token group(s): {', '.join(missing)}; "
                                            "add one to guide/reference.toml")
    unknown = [key for key in described if key not in groups]
    if unknown:
        raise ReferenceDataError(copy_path, f"entry for token group(s) that tokens.json does not have: "
                                            f"{', '.join(unknown)}")
    palette, other = [], []
    for entry in entries:
        tokens = []
        for name, token in groups[entry["id"]].items():
            if name.startswith("$"):
                continue
            resolved, alias = _resolve(name, table, tokens_path)
            tokens.append(Token(name, token["$value"], resolved, alias, token.get("$description", "")))
        group = Group(entry["id"], entry["title"], entry["intro"], tuple(tokens))
        (palette if all(HEX.match(t.resolved) for t in tokens) else other).append(group)
    return Reference(
        palette=tuple(palette), tokens=tuple(other),
        utilities=tuple((heading, guidance, tuple(sorted(rows, key=lambda row: _natural(row[0]))))
                        for heading, guidance, rows in utilities),
        legacy=tuple(legacy), white=_resolve(WHITE_TOKEN, table, tokens_path)[0],
        ink=_resolve(INK_TOKEN, table, tokens_path)[0])
