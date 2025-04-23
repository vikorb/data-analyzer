from setuptools import setup, find_packages

setup(
    name="data-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "pytest",
        "jupyter"
    ],
    entry_points={
        'console_scripts': [
            'data-analyzer=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A data analysis tool for processing CSV datasets",
    keywords="data analysis, visualization, pandas",
    python_requires='>=3.6',
)