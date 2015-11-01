import sys
import unittest
from mock import Mock
from webtest import TestApp
from bottle import *

TEMPLATE_PATH.insert(0, os.path.abspath('../views'))
sys.path.append('../')
import web

class Test(unittest.TestCase):
	def setUp(self):
		sys.path.append('../rpc')
		self.app = TestApp(web.app)
	def tearDown(self):
		pass
	
	def test_index(self):
		res = self.app.get('/')
		assert res.status == '302 Found'
		assert res.headers['Location'].endswith('/form')
		
	def test_form(self):
		res = self.app.get('/form')
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
	def test_update(self):
		res = self.app.get('/update')
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
	def test_api_serach(self):
		from search_ticket import SearchTicket
		from get_ticket import GetTicket
		from trac import Trac
		
		SearchTicket.search_ticket = Mock(return_value=[1])
		GetTicket.get_ticket = Mock(return_value=[{'id': 2, 'summary': 'test2'}, {'id': 1, 'summary': 'test1'}])
		Trac.get_team_members = Mock(return_value=['admin'])
		Trac.get_milestones = Mock(return_value=['milestone1'])
		Trac.get_components = Mock(return_value=['component1'])
		
		res = self.app.post('/api/search')
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'application/json'
		
		import json
		body = json.loads(res.body)['result']
		assert body['members'] == ['admin']
		assert body['milestones'] == ['milestone1']
		assert body['components'] == ['component1']
		assert body['tickets'] == [{'id': 1, 'summary': 'test1'}, {'id': 2, 'summary': 'test2'}]

	def test_search(self):
		from search_ticket import SearchTicket
		from get_ticket import GetTicket
		
		SearchTicket.search_ticket = Mock(return_value=[1])
		GetTicket.get_ticket = Mock(return_value=[])
		
		res = self.app.post('/search')
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
if __name__ == '__main__':
	print unittest.main()