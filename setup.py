from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gedcom555ish", package_dir={"": "src"}, packages=find_packages(where="src"), install_requires=requirements,
)
