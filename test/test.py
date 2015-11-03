import sys, os
import unittest
from mock import Mock
from webtest import TestApp
from bottle import *

root = os.path.dirname(__file__)
TEMPLATE_PATH.insert(0, os.path.join(root,os.pardir,'views'))
sys.path.append(os.path.join(root, os.pardir))
import web

class Test(unittest.TestCase):
	def setUp(self):
		sys.path.append(os.path.join(root, os.pardir, 'rpc'))
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
		
	def test_update(self):
		from update_ticket import UpdateTicket
		from trac import Trac
		
		UpdateTicket.update_ticket = Mock(return_value=[{'id': 2, 'summary': 'test2'}, {'id': 1, 'summary': 'test1'}])
		Trac.get_team_members = Mock(return_value=['admin'])
		Trac.get_milestones = Mock(return_value=['milestone1'])
		Trac.get_components = Mock(return_value=['component1'])
		
		res = self.app.post('/update')
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
	def test_api_archives(self):
		import glob
		glob.glob = Mock(return_value=glob.glob(os.path.join(root, 'test_data/archives/*.json')))
		res = self.app.get('/api/archives')
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'application/json'
		assert res.body == '{"result": [{"Date": "2015/10/31 00:10:27", "Link": "http://localhost:8080/trac/SampleProject/ticket/85", "Title": "test"}]}'
		
	def test_archives(self):
		res = self.app.get('/archives')
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
	def test_api_backlogs(self):
		from helper import Helper
		Helper.get_backlog = Mock(return_value=os.path.join(root, 'test_data', 'backlog', 'Iteration1.csv'))
		
		res = self.app.post('/api/backlogs', {'milestone': 'Iteration1'})
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'application/json'
		assert res.body == '{"result": [["Date", "Start", "2015/10/20", "2015/10/21", "2015/10/22", "2015/10/23", "2015/10/24", "2015/10/25", "2015/10/26", "2015/10/27", "2015/10/28", "2015/10/29", "2015/10/30"], ["admin", 78, 78, 69, 69, 68, 68, 56, 40, 40, 40, 0, 0], ["guest", 34, 34, 34, 34, 34, 34, 28, 20, 20, 20, 0, 0]]}'
		
	def test_api_backlogs_empty(self):
		from helper import Helper
		Helper.get_backlog = Mock(return_value=os.path.join(root, 'test_data', 'empty'))
		
		res = self.app.post('/api/backlogs', {'milestone': 'Iteration1'})
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'application/json'
		assert res.body == '{"result": []}'
		
	def test_backlog(self):
		from search_ticket import SearchTicket
		from get_ticket import GetTicket
		from trac import Trac
		from helper import Helper
		
		SearchTicket.search_ticket = Mock(return_value=[1])
		GetTicket.get_ticket = Mock(return_value=[{'id': 2, 'summary': 'test2', 'reporter': 'admin', 'due_assign': '2000/01/01', 'point': '5'}, {'id': 1, 'summary': 'test1', 'reporter': 'guest', 'due_assign': '2000/01/01', 'point': '5'}])
		Trac.get_team_members = Mock(return_value=['admin'])
		Trac.get_milestones = Mock(return_value=['milestone1'])
		Trac.get_components = Mock(return_value=['component1'])
		Helper.get_backlog = Mock(return_value=os.path.join(root,'test_data', 'create_backlog', 'none.csv'))
		
		res = self.app.post('/backlog')
		
		assert res.status == '302 Found'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'

		size = 0
		if os.name == 'nt':
			size = 43
		else:
			size = 41
		assert os.path.getsize(os.path.join(root, 'test_data', 'create_backlog', 'none.csv')) == size
				
	def test_burndown(self):
		res = self.app.get('/burndown')
		
		assert res.status == '200 OK'
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
	def test_regist(self):
		from create_ticket import CreateTicket
		from trac import Trac
		from helper import Helper

		CreateTicket.create_team_ticket = Mock(return_value=1)
		Trac.get_ticket_link = Mock(return_value='http://localhost/trac/ticket/1')
		Helper.get_archivedir = Mock(return_value=os.path.join(root, 'test_data/test_archives/'))
		Helper.get_archive_filename = Mock(return_value='test.json')
		
		res = self.app.post('/regist', {'title': 'test_ticket'})
		
		assert res.status == '303 See Other'
		assert res.headers['Location'].endswith('/archives')
		assert res.headers['Content-Type'] == 'text/html; charset=UTF-8'
		
		assert os.path.getsize(os.path.join(root, 'test_data/test_archives/test.json')) == 97

def suite():
	suite = unittest.TestSuite()
	
	suite.addTests(unittest.makeSuite(Test))
	
	from helper_test import HelperTest
	suite.addTests(unittest.makeSuite(HelperTest))
	
	return suite

if __name__ == '__main__':
	print unittest.main()