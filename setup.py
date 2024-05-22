from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

with open("scifig/__init__.py", "r") as f:
    init = f.readlines()

for line in init:
    if "__version__" in line:
        __version__ = line.split('"')[-2]

setup(
    name="SciFig",
    version=__version__,
    author="Shanlong Li",
    author_email="shanlongli@umass.edu",
    description="tools and templates for scientific figures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lslumass/SciFig",
    download_url="https://github.com/lslumass/SciFig/releases",
    platforms="Tested on Ubuntu 22.04",
    packages=["SciFig"],
    package_dir={'SciFig':'scifig'},
    install_requires=['numpy', 'matplotlib'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
    ],
)
