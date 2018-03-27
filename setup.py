from setuptools import setup, find_packages
from jasmine_runner import __version__

README = open('README.rst').read()

setup(name='jasmine-splinter-runner',
      version=__version__,
      description='jasmine runner based on splinter',
      long_description=README,
      author='CobraTeam',
      author_email='francisco@franciscosouza.net',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      install_requires=['splinter>=0.4.3,<0.8.0', 'termcolor>=1.1.0,<1.2.0'],
      tests_require=['nose', 'mocker'],
      entry_points = {
          'console_scripts' : [
              'jasmine-splinter = jasmine_runner.commands:main',
          ]
      },
     )

