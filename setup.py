"""Define metadata for Django AMP Renderer."""

# Standard Library
from pathlib import Path

# Third Party
import setuptools

long_description = Path("README.md").read_text()

setuptools.setup(
    name="django-amp-renderer",
    version="2.2.0",
    author="Chase Finch",
    author_email="chase@finch.email",
    description="Middleware for applying AMP Renderer to the output of a request in Django.",
    keywords=["Django", "AMP", "AMP Optimizer", "server-side rendering"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chasefinch/django-amp-renderer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "amp-renderer>=2.1",
        "django>=2.2.0",
    ],
)
