from setuptools import setup

setup(
    name="run-validator",
    version="0.1",
    py_modules=["RunValidator"],
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        RunValidator=RunValidator:cli
    """,
)