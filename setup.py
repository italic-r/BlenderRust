import os
import sys
import shutil
import pathlib
import subprocess

from distutils import log
from distutils.core import Command
from distutils.command.bdist import bdist
from distutils.command.install import install
from distutils.command.install_egg_info import install_egg_info
from setuptools import setup, find_packages

sys.dont_write_bytecode = True
os.environ["rust_lib_name"] = "rustlib"


class Rust(Command):
    """Sets user options."""

    description = "Build native Rust library."
    user_options = [
        ("release", None, "release mode"),
        ("target-path", None, "rust's default target path"),
        ("rust-project-path", None, "rust project's path (for cargo)"),
        ("rust-lib-name", None, "rust library's name"),
    ]

    def initialize_options(self):
        self.release = None
        self.target_path = None
        self.rust_project_path = None
        self.rust_lib_name = None

    def finalize_options(self):
        self.proj_dir = pathlib.Path(__file__).resolve().parent
        self.package_path = self.proj_dir / self.distribution.get_name()
        self.rust_project_path = self.proj_dir / "rust"
        self.target = self.rust_project_path / "target"

        if os.getenv("pyrust_release") == "1":
            self.release = True
            self.target_path = self.target / "release"
        else:
            self.target_path = self.target / "debug"

        self.rust_lib_name = os.getenv("rust_lib_name")

    def run(self):
        """Build rust library and copy to build dir."""
        self.build_rust()
        lib_file = self.get_lib_file()
        dist_name = self.distribution.get_name()

        shutil.copy(lib_file, self.proj_dir / dist_name)

        self.distribution.data_files.append((
            self.distribution.get_name(),
            ["{}/{}".format(dist_name, lib_file.name)]
        ))

    def build_rust(self):
        """Build rust library."""
        cmdlist = ["cargo", "build"]
        if self.release:
            cmdlist.append("--release")
        subprocess.check_call(cmdlist, cwd=self.rust_project_path)

    def get_lib_file(self):
        """Get library name/path from rust's default output directory."""
        prefix = {"win32": ""}.get(sys.platform, "lib")
        ext = {"darwin": "dylib", "win32": "dll"}.get(sys.platform, "so")

        return self.target_path / f"{prefix}{self.rust_lib_name}.{ext}"


class ZipBdist(bdist):
    """Create only zip archive."""

    user_options = [
        ("release", None, "release mode"),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.release = None
        self.formats = ["zip"]

    def finalize_options(self):
        super().finalize_options()
        if not self.release:
            log.info("Debug mode active...")
            os.environ["pyrust_release"] = "0"
        else:
            log.info("Release mode active...")
            os.environ["pyrust_release"] = "1"

    def run(self):
        self.run_command("rust")
        super().run()
        # Delete env var after finished with build/copy
        del os.environ["pyrust_release"]


class BlenderAddonInstall(install):
    """Blender install options."""

    def initialize_options(self):
        super().initialize_options()
        self.prefix = ""
        self.install_lib = ""


class NoEgg(install_egg_info):
    """Prevent egg-info creation."""

    def run(self):
        pass


setup(
    cmdclass={
        "rust": Rust,
        "bdist": ZipBdist,
        "install": BlenderAddonInstall,
        "install_egg_info": NoEgg,
    },
    name="pyrust",
    version="0.0.1",
    packages=find_packages("."),
    include_package_data=True,
    data_files=[
        ("pyrust", ["README.md"]),
    ],
    scripts=[],
    platforms="",
    zip_safe=False,
)
