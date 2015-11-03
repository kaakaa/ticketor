import sys, os
import unittest
from mock import Mock
from webtest import TestApp
from bottle import *

root = os.path.dirname(__file__)
sys.path.append(os.path.join(root, os.pardir))
from helper import Helper

class HelperTest(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	def test_daterange(self):
		from datetime import datetime, timedelta
		
		start = datetime.strptime('2015/10/1', '%Y/%m/%d')
		end = datetime.strptime('2015/10/3', '%Y/%m/%d')
		
		range = Helper.daterange(start, end)
		assert range == ['2015/10/01', '2015/10/02']
		
	def test_daterange_empty(self):
		from datetime import datetime
		
		start = datetime.strptime('2015/10/1', '%Y/%m/%d')
		end = datetime.strptime('2015/10/1', '%Y/%m/%d')
		
		range = Helper.daterange(start, end)
		
		assert range == []
		
	def test_daterange_illegal(self):
		from datetime import datetime
		
		start = datetime.strptime('2015/10/2', '%Y/%m/%d')
		end = datetime.strptime('2015/10/1', '%Y/%m/%d')
		
		range = Helper.daterange(start, end)
		
		assert range == []
	
	def test_calculate_data(self):
		daterange = ['2015/10/01', '2015/10/02']
		member = 'admin'

		tickets = [{
			'reporter': 'admin',
			'due_assign': '2015/10/01',
			'point': '1'}]
		
		backlog = Helper.calculate_data(tickets, member, daterange)
		
		assert backlog == ['admin', '1', '0', '0']
		
	def test_calculate_data_multiticket(self):
		start = datetime.strptime('2015/10/1', '%Y/%m/%d')
		end = datetime.strptime('2015/10/3', '%Y/%m/%d')
		daterange = ['2015/10/01', '2015/10/02']
		member = 'admin'

		tickets = [
			{
				'reporter': 'admin',
				'due_assign': '2015/10/01',
				'point': '10'
			},
			{
				'reporter': 'admin',
				'due_assign': '2015/10/02',
				'point': '5'
			},
			{
				'reporter': 'admin',
				'due_assign': '2015/10/03', # out of date
				'point': '5'
			},
			{
				'reporter': 'guest', # assign others
				'due_assign': '2015/10/01',
				'point': '8'
			}]
		
		backlog = Helper.calculate_data(tickets, member, daterange)
		assert backlog == ['admin', '15', '5', '0']
		
	def test_calculate_data_empty(self):
		start = datetime.strptime('2015/10/1', '%Y/%m/%d')
		end = datetime.strptime('2015/10/3', '%Y/%m/%d')
		daterange = ['2015/10/01', '2015/10/02']
		member = 'admin'

		tickets = []
		
		backlog = Helper.calculate_data(tickets, member, daterange)
		
		assert backlog == ['admin', '0', '0', '0']
		
	def test_calculate_data_noassign(self):
		start = datetime.strptime('2015/10/1', '%Y/%m/%d')
		end = datetime.strptime('2015/10/3', '%Y/%m/%d')
		daterange = ['2015/10/01', '2015/10/02']
		member = 'admin'

		tickets = [
			{
				'reporter': 'guest',
				'due_assign': '2015/10/01',
				'point': '10'
			},
			{
				'reporter': 'guest',
				'due_assign': '2015/10/02',
				'point': '5'
			}]
		
		backlog = Helper.calculate_data(tickets, member, daterange)
		
		assert backlog == ['admin', '0', '0', '0']
		
if __name__ == '__main__':
	print unittest.main()