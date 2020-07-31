#!/usr/bin/env python3

from datetime import datetime as dt
from setuptools import setup, find_packages
import ledfx.consts as const
from setuptools import Extension, setup
from Cython.Build import cythonize

PROJECT_PACKAGE_NAME = 'ledfx'
PROJECT_VERSION = const.PROJECT_VERSION
PROJECT_LICENSE = 'The MIT License'
PROJECT_AUTHOR = 'Austin Hodges'
PROJECT_AUTHOR_EMAIL = 'austin.b.hodges@gmail.com'
PROJECT_URL = 'http://github.com/ahodges9/ledfx'

# Need to install numpy first
SETUP_REQUIRES = [
	'numpy>=1.13.3'
]

INSTALL_REQUIRES = [
	'numpy>=1.13.3',
	'voluptuous==0.11.1',
	'pyaudio>=0.2.11',
	'sacn==1.3',
	'aiohttp==3.3.2',
	'aiohttp_jinja2==1.0.0',
	'requests>=2.22.0',
	'pyyaml>=5.1',
	'aubio>=0.4.8',
	'pypiwin32>=223;platform_system=="Windows"'
]

setup(
	name=PROJECT_PACKAGE_NAME,
	version=PROJECT_VERSION,
	license=PROJECT_LICENSE,
	author=PROJECT_AUTHOR,
	author_email=PROJECT_AUTHOR_EMAIL,
	url=PROJECT_URL,
	install_requires=INSTALL_REQUIRES,
	setup_requires=SETUP_REQUIRES,
	python_requires=const.REQUIRED_PYTHON_STRING,
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': [
			'ledfx = ledfx.__main__:main'
		]
	},
	package_data={
		'ledfx_frontend': ['*'],
		'': ['*.npy']
	},
	ext_modules=cythonize([
		Extension(
			"ledfx.effects.noteFinder",
			[
				"ledfx/effects/noteFinder.pyx",
				"ledfx/effects/colorchord/colorchord2/dft.c",
				"ledfx/effects/colorchord/colorchord2/notefinder.c",
				"ledfx/effects/colorchord/colorchord2/parameters.c",
				"ledfx/effects/colorchord/colorchord2/chash.c",
				"ledfx/effects/colorchord/colorchord2/decompose.c",
				"ledfx/effects/colorchord/colorchord2/util.c",
				"ledfx/effects/colorchord/colorchord2/filter.c",
				"ledfx/effects/colorchord/embeddedcommon/DFT32.c",
			],
			include_dirs=[
				"ledfx/effects/colorchord/colorchord2/cnfa",
				"ledfx/effects/colorchord/colorchord2/rawdraw",
				"ledfx/effects/colorchord/embeddedcommon",
				"ledfx/effects/colorchord/colorchord2"
			],
			extra_compile_args=[
				"-DICACHE_FLASH_ATTR=",
				"-DINCLUDING_EMBEDDED=",
				"-flto",
				"-Wall",
				"-ffast-math",
				"-g",
			],
			libraries=[
				"m",
			],
			depends=[
				"ledfx/effects/cnoteFinder.pxd"
			],
		)
	])
)
