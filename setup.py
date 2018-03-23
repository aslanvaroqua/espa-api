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
          'falcon==1.4.1',
          'mock==2.0.0',
          'paramiko==2.4.1',
          'psycopg2==2.7.4',
          'python-memcached==1.59',
          'PyYAML==3.12',
          'passlib==1.7.1',
          'requests==2.18.4',
          'simplejson==3.13.2',
          'six==1.11.0',
          'suds-py3==1.3.3.0',
          'validate-email==1.3',
          'validictory==1.1.2',
      ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[test]
      extras_require={
          'test': [
              'coverage==4.5.1',
              'cov-core==1.15.0',
              'nose2==0.7.4',
              'nose2-cov==1.0a4',
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
