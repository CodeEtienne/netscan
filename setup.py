from setuptools import setup, find_packages
from pathlib import Path


def get_version():
    version_file = Path(__file__).parent / "netscan" / "__init__.py"
    with open(version_file) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')


setup(
    name="netscan",
    version=get_version(),
    description="A simple network scanner",
    author="Etienne",
    author_email="etienne.jannin@gmail.com",
    packages=find_packages(),
    install_requires=[
        "rich",
        "netifaces",
    ],
    entry_points={
        "console_scripts": [
            "netscan=netscan.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
