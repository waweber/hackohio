from setuptools import setup, find_packages

reqs = [
    "pyramid",
    "pyramid_jinja2",
    "waitress",
    "tweepy",
    "pyramid_debugtoolbar",
]

setup(
    name="hackohio",
    version="0.0.0",
    packages=find_packages(),

    install_requires=reqs,

    entry_points={
        "paste.app_factory": [
            "main = hackohio.wsgi:main",
        ],
    },
)
