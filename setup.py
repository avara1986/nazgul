import Cython.Distutils
from Cython.Build import cythonize
from setuptools import find_packages, setup

extra_compile_args = [
    "-g",
    "-O0",
    "-Wall",
    "-Wpedantic",
]

setup(
    name='py-nazgul',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['Click==8.1.3', 'Cython==0.29.30'],
    entry_points={
        'console_scripts': [
            'nazgul = nazgul.cli:cli',
        ],
    },
    ext_modules=cythonize(
        [
            Cython.Distutils.Extension(
                "nazgul.nazgul",
                sources=["nazgul/nazgul.pyx", "nazgul/src/Task.cpp"],
                include_dirs=["nazgul/src"],
                libraries=["sqlite3", "pthread"],
                language="c++",
                extra_compile_args=extra_compile_args,
            ),
        ]
    ),
)
