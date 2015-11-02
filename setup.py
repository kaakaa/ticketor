from setuptools import setup, find_packages
from pip.req import parse_requirements
import sys

sys.path.append('./rpc')
sys.path.append('./test')

install_reqs = parse_requirements('./requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
	name = 'trac-team-task-register',
	version = '0.1',
	description = 'Manipulate trac tickets',
	packages = find_packages(),
	install_requires=reqs,
	test_suite = 'test.suite'
)