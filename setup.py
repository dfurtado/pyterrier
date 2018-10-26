#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'jinja2>=2.10', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Daniel Furtado",
    author_email='daniel@dfurtado.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="The web framework that favorite conventions over configurations",
    entry_points={
        'console_scripts': [
            'pyterrier=pyterrier.pyterrier_cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyterrier',
    name='pyterrier',
    packages=find_packages(include=[
        'pyterrier',
        'pyterrier.app_template',
        'pyterrier.cli',
        'pyterrier.core',
        'pyterrier.encoders',
        'pyterrier.http',
        'pyterrier.renderers',
        'pyterrier.validators']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dfurtado/pyterrier',
    version='0.1.0',
    zip_safe=False,
)
