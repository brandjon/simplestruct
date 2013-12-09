from setuptools import setup

import struct

setup(
    name='struct',
    version=struct.__version__,
    
    author='Jon Brandvein',
    license='MIT License',
    description='A Python library for defining struct-like classes',
    
    packages=['struct'],
)
