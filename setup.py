from setuptools import setup

setup(
    name="typkg",
    version="0.1.0",
    py_modules=["main"],
    install_requires=["toml", "gitpython"],
    entry_points={"console_scripts": ["typkg = main:main"]},
    author="Tch1b0",
    description="tiny and simple typst (git-repo-)package installer",
)
