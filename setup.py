import os
from setuptools import find_packages, setup

with open(os.path.join('.', 'VERSION')) as version_file:
    version = version_file.read().strip()
    print(f"version: {version}")
setup(
    name='gresq',
    version=version,
    long_description=open('README.md').read(),
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
          'gui_scripts': [
              'gresq = gresq.__main__:main'
          ]
      },
    install_requires=[
        "sqlalchemy>=1.3.23",
        "pymysql>=1.0.2",
    ],
    test_requires=[
        "pytest",
        "factory_boy"
    ],
    python_requires=">3.8",
)
