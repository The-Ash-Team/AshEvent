from setuptools import setup, find_packages
from re import finditer

with open(file="README.md", mode="r", encoding="utf-8") as f:
    long_description = f.read()
with open(file="ashevent/__init__.py", mode="r", encoding="utf-8") as f:
    version = next(finditer(r"__version__[ ]*=[ ]*[\'\"](.*?)[\"\']", f.read())).group(1)

setup(
    name="ashevent", version=version, author="Za08",
    description="A simple event system in Python",
    long_description=long_description, long_description_content_type="text/markdown",
    url="https://github.com/The-Ash-Team/AshEvent", license="MIT",
    packages=find_packages()
)
