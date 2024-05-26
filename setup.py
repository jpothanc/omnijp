from setuptools import setup, find_packages

setup(
    name='omnijp',
    version='2.3.0',
    packages=find_packages(),
    install_requires=[
        'retry>=0.9.2',
        'requests>=2.31.0',
        'pymssql>=2.3.0',
        'psycopg2>=2.9.9'
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
)
