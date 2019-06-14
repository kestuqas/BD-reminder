from setuptools import setup

setup(
	name='bd-reminder',
	version='1.0',
	py_modules=['trial'],
	install_requires=[
		'Click',
		'Datetime',
		'emails',
		'config'
	],
	entry_points='''
		[console_scripts]
		reminder=reminder:validate_send
	''',
)
