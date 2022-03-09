from setuptools import find_packages, setup

setup(
    name="zyte-common-items",
    version="0.1.0",
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
    install_requires=[
        "attrs",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.7",
)
