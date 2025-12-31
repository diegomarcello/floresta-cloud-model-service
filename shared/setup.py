from setuptools import setup, find_packages

setup(
    name="floresta_shared",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "redis",
        "pymongo",
    ],
)
