"""Define metadata for Django AMP Renderer."""

# Third Party
import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="django-amp-renderer",
    version="2.0.1",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "amp-renderer>=2.0.0",
        "django>=2.2.0",
    ],
)
