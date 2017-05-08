import codecs
import os.path
from setuptools import find_packages, setup

NAME = 'masterconfigparser'
with codecs.open(os.path.join(NAME, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=version,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    author='Brendan Zerr',
    author_email='bzerr@brainwire.ca',
    description='Master/local INI parser (ConfigParser compatible)',
    long_description=long_description,
    url='',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    license='MIT',
    classifiers=[]
)
