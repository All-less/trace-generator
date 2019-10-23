from setuptools import setup, find_packages

setup(
    name = 'spar',
    packages = find_packages(exclude=('config')),
    version = '0.0.1',
    description = 'A CLI tool for generating controllable cluster trace.',
    author = 'All-less',
    author_email = 'all.less.mail@gmail.com',
    url = 'https://github.com/All-less/trace-generator',
    install_requires = [
        'click',
        'scipy',
        'crayons',
        'numpy'
    ],
    entry_points = {
        'console_scripts': [
            'spar=spar.cli:main'
        ]
    },
    keywords = [ 'cluster trace', 'cloud computing' ],
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
