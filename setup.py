from setuptools import setup, find_packages

setup(
    name='omnijp',
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'retry>=0.9.2',
        'requests>=2.31.0'
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
)
