from setuptools import find_packages, setup
# Import this after setuptools or it will fail
import Cython.Distutils
from Cython.Build import cythonize  # noqa: I100

extra_compile_args = [
    "-g",
    "-O0",
    "-Wall",
    "-Wpedantic",
]

if __name__ == "__main__":
    setup(
        ext_modules=cythonize(
            [
                Cython.Distutils.Extension(
                    "nazgul.core",
                    sources=["nazgul/core.pyx", "nazgul/src/Task.cpp"],
                    include_dirs=["nazgul/src"],
                    libraries=["sqlite3", "pthread"],
                    language="c++",
                    extra_compile_args=extra_compile_args,
                ),
            ]
        )
    )
