from setuptools import setup, find_packages

setuptools.setup(
           name='paas_staytus_scripts',
           version='0.0.1',
           packages=find_packages(exclude=['etc']),
           data_files=[('etc/paas-staytus-scripts',[ 'etc/config.ini'])],
           entry_points={
               'console_scripts': [
                  'paas-staytus-health=paas_staytus_scripts.health_test:main'
                ]
           }
)
