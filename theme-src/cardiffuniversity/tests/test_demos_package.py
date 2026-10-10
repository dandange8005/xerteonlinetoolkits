"""The demos packaged as a hidden Xerte theme that an admin can upload. See tools/build-demos-package.py."""
import re
import tempfile
import unittest
import zipfile
from pathlib import PurePosixPath

import support
import theme_css
from html_tree import parse

DEMOS = support.THEME / "demos"
NAME = "cardiffuniversity-demos"
# What Xerte's upload (functions.php x_check_zip) refuses, plus the files that would break the upload.
FORBIDDEN_EXTENSIONS = {"php", "php1", "php2", "php3", "php4", "php5", "php6", "php7", "php8", "phar", "inc", "htaccess"}
CSS_REFERENCE = re.compile(r'''url\(["']?([^"')]+)["']?\)''')


class DemosPackageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.zip_path = support.load_tool("build-demos-package").build(support.Path(cls.tmp.name) / f"{NAME}.zip")
        cls.zip = zipfile.ZipFile(cls.zip_path)
        cls.names = [n for n in cls.zip.namelist() if not n.endswith("/")]

    @classmethod
    def tearDownClass(cls):
        cls.zip.close()
        cls.tmp.cleanup()

    def text(self, name):
        return self.zip.read(f"{NAME}/{name}").decode("utf-8")

    def test_the_file_name_has_only_one_dot(self):
        # upload_theme.php reads the extension from the second part of the name split on dots.
        self.assertEqual(self.zip_path.name.count("."), 1)
        self.assertEqual(self.zip_path.suffix, ".zip")

    def test_everything_sits_in_one_folder_named_like_the_info_file(self):
        self.assertTrue(all(n.startswith(f"{NAME}/") for n in self.names), self.names[:5])
        infos = [n for n in self.names if n.endswith(".info")]
        self.assertEqual(infos, [f"{NAME}/{NAME}.info"])

    def test_the_info_file_names_the_theme(self):
        info = dict(line.split(":", 1) for line in self.text(f"{NAME}.info").splitlines() if ":" in line)
        self.assertEqual(info["name"].strip(), NAME)
        self.assertTrue(info["display name"].strip())

    def test_nothing_the_upload_would_refuse(self):
        bad = [n for n in self.names
               if n.rsplit(".", 1)[-1].lower() in FORBIDDEN_EXTENSIONS or ".." in n or n.startswith("/")]
        self.assertEqual(bad, [])

    def test_no_hidden_files_travel_in_the_zip(self):
        # hidden.info would also end in .info and confuse the uploader's theme-name detection.
        hidden = [n for n in self.names if PurePosixPath(n).name.startswith(".") or PurePosixPath(n).name == "hidden.info"]
        self.assertEqual(hidden, [])

    def test_every_demo_page_is_in_the_package(self):
        pages = {p.name for p in DEMOS.glob("*.html")}
        self.assertEqual({PurePosixPath(n).name for n in self.names if n.endswith(".html")}, pages)
        self.assertIn(f"{NAME}/index.html", self.names)

    def test_every_local_reference_resolves_inside_the_package(self):
        # The package is served from themes/site/<name>/, so nothing may reach outside its own folder.
        files = set(self.names)
        missing = []
        for name in self.names:
            if name.endswith(".html"):
                tree = parse(self.zip.read(name).decode("utf-8"))
                targets = [e.attrs.get("href") for e in tree.find_all("link") + tree.find_all("a")]
                targets += [e.attrs.get("src") for e in tree.find_all("script") + tree.find_all("img")]
            elif name.endswith(".css"):
                targets = CSS_REFERENCE.findall(re.sub(r"/\*.*?\*/", "", self.zip.read(name).decode("utf-8"), flags=re.S))
            else:
                continue
            for target in filter(None, targets):
                if re.match(r"(https?:|data:|mailto:|//|#)", target):
                    continue
                path = PurePosixPath(name).parent
                for part in target.split("#")[0].split("?")[0].split("/"):
                    path = path.parent if part == ".." else path if part in ("", ".") else path / part
                if str(path) not in files:
                    missing.append(f"{name} -> {target}")
        # Two files Bootstrap 2's stylesheets name but the demos never shipped, so they were never loaded.
        missing = [m for m in missing if "glyphicons-halflings" not in m and not m.endswith("-> editorstyles.css")]
        self.assertEqual(missing, [])

    def test_the_package_carries_the_current_compiled_theme(self):
        self.assertEqual(self.zip.read(f"{NAME}/cardiffuniversity.css"), theme_css.CSS.read_bytes())
        self.assertEqual(self.zip.read(f"{NAME}/logo_left.svg"), (theme_css.CSS.parent / "logo_left.svg").read_bytes())

    def test_font_awesome_travels_with_the_package(self):
        # The server's copy of Font Awesome may sit in a different folder, so the package brings its own.
        self.assertIn(f"{NAME}/fontawesome-6.6.0/css/all.min.css", self.names)
        self.assertTrue(any(n.startswith(f"{NAME}/fontawesome-6.6.0/webfonts/fa-solid-900.") for n in self.names))

    def test_pages_differ_from_the_demos_only_in_where_they_find_the_theme(self):
        # Edit the demos, never the package: the only rewrites are the three theme and font links.
        for page in DEMOS.glob("*.html"):
            source = page.read_text(encoding="utf-8")
            packaged = self.text(page.name)
            for old, new in (("../../../themes/site/cardiffuniversity/cardiffuniversity.css", "cardiffuniversity.css"),
                             ("../../../themes/site/cardiffuniversity/logo_left.svg", "logo_left.svg"),
                             ("../../../modules/common/fontawesome-6.6.0/", "fontawesome-6.6.0/")):
                source = source.replace(old, new)
            self.assertEqual(packaged, source, page.name)


if __name__ == "__main__":
    unittest.main()
