from setuptools import setup, find_packages

setup(
    name="sql_column_extractor",          # your package name
    version="0.2.0",                      # bump version as needed
    author="Krishnan Nagarajan",
    author_email="krishgenius1@yahoo.com",
    description="A library to extract SQL columns from queries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/krishgenius/sql_column_extractor",  # update with your repo
    license="MIT",
    packages=find_packages(),             # auto-detects the sql_column_extractor folder
    python_requires=">=3.7",              # adjust to your Python version support
    install_requires=[
        # list dependencies here, e.g.:
        # "sqlparse>=0.4.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
