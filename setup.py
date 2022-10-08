import os
from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

def read_version():
    """Read the version from the VERSION.txt in the root folder."""
    with open(os.path.join(here, "VERSION.txt")) as fh:
        return fh.readline().strip()

setup(
    name="JDS6600",
    version=read_version(),
    description="Python module to communicate with the JDS6600 DDS Signal Generator.",
    #url="",
    author="Wim De Hul",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],        
    keywords="jsd6600, electronics, signal generator",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=["pyserial"],
    #project_urls={  # Optional
    #    "Bug Reports": "https://github.com/pypa/sampleproject/issues",
    #    "Funding": "https://donate.pypi.org",
    #    "Say Thanks!": "http://saythanks.io/to/example",
    #    "Source": "https://github.com/pypa/sampleproject/",
    #},
)