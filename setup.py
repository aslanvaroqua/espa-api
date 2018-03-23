from setuptools import setup

def version():
    with open('version.txt') as f:
        return f.read()

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='espa-api',
      version=version(),
      description='API for the ESPA ordering system',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='usgs eros lsrd espa',
      url='http://github.com/usgs-eros/espa-api',
      author='USGS EROS ESPA',
      author_email='',
      license='Unlicense',
      packages=None,
      install_requires=[
          'falcon',
          'hug',
          'mock',
          'paramiko',
          'psycopg2',
          'python-memcached',
          'PyYAML',
          'passlib',
          'requests',
          'simplejson',
          'six',
          'suds-py3',
          'validate-email',
          'validictory',
          'uWSGI',
      ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[test]
      extras_require={
          'test': [
              'pytest',
              'pytest-cov',
              'vcrpy',
              'hypothesis',
                  ],
          'doc': [],
          'dev': [],
      },
      entry_points={
          'console_scripts': [
          ],
      },
      include_package_data=True,
      zip_safe=False
)
