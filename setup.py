from setuptools import setup, find_packages

reqs = [
    "pyramid",
    "waitress",
]

setup(
    name="hackohio",
    version="0.0.0",
    packages=find_packages(),

    install_requires=reqs,
)
