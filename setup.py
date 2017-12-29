#! /user/bin/python
# coding:UTF-8

from setuptools import setup, find_packages
setup(
    name='PyDbgEng',
    version="0.0.5",
    description='A python wrapper of debug engines on windows, linux or osx.',
    author='WalkerFuz',
    packages=find_packages(),
    include_package_data=True,
)
