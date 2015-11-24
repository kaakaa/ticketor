from setuptools import setup, find_packages
from pip.req import parse_requirements
import sys
from docs.build_apidoc import BuildApiCommand

sys.path.append('./')
sys.path.append('./app')
sys.path.append('./app/rpc')
sys.path.append('./docs')

install_reqs = parse_requirements('./requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]
long_description = open('README.md', 'r').read().decode('utf-8')

name = 'ticketor'
version = '0.1'

setup(
	# Project Infomation
	name = name,
	version = version,
	description = 'Manipulate trac tickets',
	long_description=long_description,

	# Testing
	packages = find_packages(),
	install_requires=reqs,
	test_suite = 'test.suite',

	# Documentation
	setup_requires=['Sphinx'],
	cmdclass = {
		'build_apidoc': BuildApiCommand
	}
)
