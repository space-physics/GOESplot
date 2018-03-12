#!/usr/bin/env python
install_requires = ['python-dateutil','numpy','imageio']
tests_require = ['pytest','nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='GOES_quickplot',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/goes-quick-plot',
      long_description=open('README.rst').read(),
      description='easily download and plot GOES weather satellite data',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'plots':['cartopy','matplotlib'],
                      'io':['netCDF4']},
      python_requires='>=3.6',
	  )

