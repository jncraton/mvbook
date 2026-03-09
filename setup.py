from setuptools import setup, find_packages

setup(
  name='mvbook',
  version='0.1.0',
  packages=find_packages(),
  entry_points={
    'console_scripts': [
      'mvbook=mvbook.cli:main'
    ]
  },
  install_requires=[
    'requests>=2.28.0'
  ]
)
