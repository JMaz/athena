from setuptools import setup

setup(
	name='Athena_CTF',
	version='1.0',
	py_modules=['athena'],
	install_requires=['Click','socketIO-client'],
	entry_points='''
		[console_scripts]
		athena=athena:cli
	''',
)
