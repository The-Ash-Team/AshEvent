from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AshEvent-Za08', version='0.2', author='Za08',
    description='A simple event system in Python',
    long_description=long_description, long_description_content_type='text/markdown',
    url='https://github.com/The-Ash-Team/AshEvent', license='MIT',
    packages=find_packages()
)
