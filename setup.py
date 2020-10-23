from setuptools import setup, find_packages

setup(
    name="raspcuterie",
    version="0.1.0",
    py_modules=["raspcuterie"],
    packages=find_packages(),
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        raspcuterie-cli=raspcuterie.cli:cli
    """,
)
