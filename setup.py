from setuptools import setup, find_packages

setup(
    name="linkedin_job_scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        "pandas>=1.3.0",
        "fake-useragent>=1.1.3",
        "python-dateutil>=2.8.2",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "linkedin_scraper=scraper:main"
        ]
    },
)
