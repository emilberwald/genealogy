from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="genealogy", package_dir={"": "src"}, packages=find_packages(where="src"), install_requires=requirements,
)
