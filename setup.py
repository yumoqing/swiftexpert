# -*- coding: utf-8 -*-


from distutils.core import setup
from setuptools import setup, find_packages

# usage:
# python setup.py bdist_wininst generate a window executable file
# python setup.py bdist_egg generate a egg file
# Release information about eway

version = "0.1.0"
description = "swiftexpert"
author = "yumoqing"
email = "yumoqing@gmail.com"

packages=find_packages()
package_data = {
	"swiftexpert":['conf/*/*.xlsx','conf/*.xlsx'],
}

setup(
    name="swiftexpert",
    version=version,
    
    # uncomment the following lines if you fill them out in release.py
    description=description,
    author=author,
    author_email=email,
   
    install_requires=[
    ],
    packages=packages,
    package_data=package_data,
    keywords = [
    ],
    data_files=[
    ],
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python3.5',
        'Topic :: SQL execute :: Libraries :: Python Modules',
    ],
	platforms= 'any'
)
