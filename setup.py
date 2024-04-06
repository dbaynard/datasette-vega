from distutils.core import Command
from setuptools import setup
from subprocess import check_output
from wheel.bdist_wheel import bdist_wheel
import os

VERSION = "0.7a0"
ROOT = os.path.dirname(os.path.abspath(__file__))


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


class BdistWheelWithBuildStatic(bdist_wheel):
    def run(self):
        self.run_command("build_static")
        return bdist_wheel.run(self)


class BuildStatic(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        check_output(["mkdir", "-p", "datasette_vega/static"], cwd=ROOT)
        check_output(
            "cp @npm_build@/static/js/* datasette_vega/static/", shell=True, cwd=ROOT
        )
        check_output(
            "cp @npm_build@/static/css/* datasette_vega/static/", shell=True, cwd=ROOT
        )


setup(
    name="datasette-vega",
    description="A Datasette plugin that provides tools for generating charts using Vega",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-vega",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_vega"],
    entry_points={
        "datasette": ["vega = datasette_vega"],
    },
    package_data={
        "datasette_vega": [
            "static/*.js",
            "static/*.css",
            "static/*.map",
        ],
    },
    cmdclass={
        "bdist_wheel": BdistWheelWithBuildStatic,
        "build_static": BuildStatic,
    },
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx"]},
)
