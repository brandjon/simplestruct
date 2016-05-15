from setuptools import setup

setup(
    name =          'SimpleStruct',
    version =       '0.2.2',
    url =           'https://github.com/brandjon/simplestruct',
    
    author =        'Jon Brandvein',
    author_email =  'jon.brandvein@gmail.com',
    license =       'MIT License',
    description =   'A library for defining struct-like classes',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    packages =      ['simplestruct'],
    
    test_suite =    'tests',
)
