from setuptools import setup, find_packages


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
    packages=["SciFig"],
    package_dir={"SciFig": "scifig"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib>=3.1.0",
        "numpy>=1.17.0",
    ],
)
