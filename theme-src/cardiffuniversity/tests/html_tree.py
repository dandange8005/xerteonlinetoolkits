"""A tiny HTML tree for tests: parse a page, then find elements by tag, class or attribute."""
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Element:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def iter(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.iter()

    def find_all(self, tag=None, cls=None, **attrs):
        wanted = {key.replace("_", "-"): value for key, value in attrs.items()}
        return [e for e in self.iter()
                if (tag is None or e.tag == tag) and (cls is None or cls in e.classes)
                and all(e.attrs.get(key) == value for key, value in wanted.items())]

    def find(self, tag=None, cls=None, **attrs):
        found = self.find_all(tag, cls, **attrs)
        if not found:
            raise AssertionError(f"no element matching tag={tag} class={cls} {attrs}")
        return found[0]


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = self.current = Element("#root", [])

    def handle_starttag(self, tag, attrs):
        element = Element(tag, attrs, self.current)
        self.current.children.append(element)
        if tag not in VOID:
            self.current = element

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Element(tag, attrs, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse(text):
    builder = _Builder()
    builder.feed(text)
    builder.close()
    return builder.root
