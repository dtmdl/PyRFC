from tests.config import latest_python_version
import pytest
import sys
from os import listdir
from os.path import isfile, join
from contextlib import suppress

with suppress(ModuleNotFoundError):
    import tomllib


@pytest.mark.skipif(
    "tomllib" not in sys.modules or "darwin" not in sys.platform or sys.version_info < latest_python_version,
    reason="package check on latest python only",
)
class TestPackage:
    def setup_class(self):
        self.package_name = "pyrfc"
        with open("pyproject.toml", "rb") as file:
            pyproject = tomllib.load(file)
        self.package_name = pyproject["project"]["name"]
        self.version = pyproject["project"]["version"]
        # assert subprocess.call(["bash", "tests/build_test.sh"]) == 0

    def test_wheel_package(self):
        package_path = join(
            ".tox",
            "pack",
            "tmp",
            self.package_name,
        )
        package_files = [fn for fn in listdir(package_path) if isfile(join(package_path, fn))]
        print(package_files)
        exts = set()
        # no cython and c sources, only python and 'so'
        for fn in package_files:
            ext = fn.rsplit(".", 1)[1]
            assert ext in ["py", "so"]
            exts.add(ext)
        assert "py" in exts
        assert "so" in exts

    def test_sdist_package(self):
        sdist_path = join(
            ".tox",
            "pack",
            "tmp",
            f"{self.package_name}-{self.version}",
            "src",
            self.package_name,
        )
        sdist_files = [fn for fn in listdir(sdist_path) if isfile(join(sdist_path, fn))]
        print(sdist_files)
        exts = set()
        # python, cython and c sources, no 'so'
        for fn in sdist_files:
            ext = fn.rsplit(".", 1)[1]
            assert ext in [
                "py",
                "pxd",
                "pyx",
                "cpp",
            ]
            exts.add(ext)
        assert "py" in exts
        assert "pxd" in exts
        assert "pyx" in exts
        assert "cpp" in exts
