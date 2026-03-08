from setuptools import setup, find_packages

setup(
    name="debug-search",
    version="0.1",
    py_modules=["cli"],
    packages=find_packages(),
    install_requires=[
        "whoosh",
        "watchdog"
    ],
    entry_points={
        "console_scripts": [
            "debug-search=cli:main"
        ]
    },
)