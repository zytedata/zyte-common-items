from os.path import dirname, join

from setuptools import find_packages, setup

with open(join(dirname(__file__), "zyte_common_items/VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

setup(
    name="zyte-common-items",
    version=version,
    description="Item definitions for Zyte API schema",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="Zyte Group Ltd",
    author_email="info@zyte.com",
    url="https://github.com/zytedata/zyte-common-items",
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    package_data={
        "zyte_common_items": ["py.typed", "VERSION"],
    },
    install_requires=[
        "attrs>=21.3.0",
        "itemadapter>=0.8.0",
        "web-poet>=0.7.0",
        "zyte-parsers",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.8",
)
