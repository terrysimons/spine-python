#!/usr/bin/env python

from distutils.core import setup

setup(name='spine-python',
      version='1.0b1',
      description='A Pure Python Spine runtime.',
      author='Terry Simons',
      author_email='terry.simons@gmail.com',
      url='https://github.com/terrysimons/spine-python/spine-python',
      package_dir={'spine': 'src'},
      packages=['spine', 'spine.Atlas', 'spine.Animation'],
     )
