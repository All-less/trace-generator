from setuptools import setup, find_packages

setup(
    name = 'spar',
    packages = find_packages(exclude=('config')),
    version = '0.0.6',
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
    license="MIT",
    keywords = [ 'cluster trace', 'cloud computing' ],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    include_package_data=True
)
