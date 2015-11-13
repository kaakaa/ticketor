import os
from datetime import datetime,timedelta

class Helper:
	@staticmethod
	def get_backlog(root, file):
		return os.path.join(root, '..', 'data', 'backlog', file)
	@staticmethod
	def get_archivedir(root):
		return os.path.join(root, '..', 'data', 'archives')
	@staticmethod
	def get_archive_filename(now):
		return now.strftime("%Y%m%d%H%M%S") + ".json"
	
	@staticmethod
	def daterange(start, end):
		dates = []
		for n in range((end - start).days):
			dates.append(start + timedelta(n))
		return map(lambda d: d.strftime('%Y/%m/%d'), dates)
		
	@staticmethod
	def calculate_backlog(tickets, member, daterange, date_field):
		my_tickets = [t for t in tickets if t['reporter'] == member]
		backlogs = {}
		for date in daterange:
			sum_point = sum([float(t['point']) for t in my_tickets if t.has_key(date_field) and t[date_field] == date])
			backlogs[date] = str(int(sum_point))
		return backlogs

	@staticmethod
	def calculate_burndown_estimated(backlogs):
		burndown = {}
		point = sum([int(v) for v in backlogs.values()])
		all_point = point
		for k,v in sorted(backlogs.items()):
			point -= int(v)
			burndown[k] = str(point)
			
		burndown['Start'] = str(all_point)
		return burndown
		
	@staticmethod
	def calculate_data(tickets, member, daterange):
		from helper import Helper
		
		backlogs = Helper.calculate_backlog(tickets, member, daterange, 'due_assign')
		burndown = Helper.calculate_burndown_estimated(backlogs)
		
		csv = [member, burndown['Start']]
		for d in sorted(daterange):
			csv.append(burndown[d])
		return csv
	
	@staticmethod
	def calculate_burndown_actual(backlogs, total_point):
		burndown = {}
		point = int(total_point)
		for k,v in sorted(backlogs.items()):
			point -= int(v)
			burndown[k] = str(point)
			
		burndown['Start'] = str(total_point)
		return burndown
		
		
	@staticmethod
	def calculate_data_actual(tickets, member, daterange, total_point):
		from helper import Helper
		
		backlogs = Helper.calculate_backlog(tickets, member, daterange, 'closed')
		burndown = Helper.calculate_burndown_actual(backlogs, total_point)
		
		csv = [member, burndown['Start']]
		for d in sorted(daterange):
			csv.append(burndown[d])
		return csv
	
