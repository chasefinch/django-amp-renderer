# -*- coding: UTF-8 -*-
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-amp-renderer',
    version='1.2.1',
    author='Chase Finch',
    author_email='chase@finch.email',
    description='Middleware for applying AMP Renderer to the output of a request in Django.',
    keywords=['Django', 'AMP', 'AMP Optimizer', 'server-side rendering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chasefinch/django-amp-renderer',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.7',
    install_requires=[
        'future;python_version<="2.7"',
        'amp-renderer>=1.1.2',
        'django>=1.11.0',
    ],
)
