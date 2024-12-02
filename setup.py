from setuptools import setup, find_packages

setup(
  name="nba_2_sample",
  version="0.1",
  packages=find_packages(),
  install_requires=[
    "pandas",
    "requests",
    "beautifulsoup4",
    "matplotlib",
    "scikit-learn",
    "pytest",
  ],
  entry_points={
    "console_scripts": [
      "nba-scrape = nba_2_sample.data_scraping:main",
    ]
  },
  test_suite="tests",
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  author="Caleb Carlyle",
  author_email="chc38@byu.edu",
  description="A package for scraping and analyzing within-player data in the NBA",
  url="https://github.com/chcarlyle/nba_2_sample",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
