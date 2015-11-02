from datetime import datetime,timedelta

class Helper:
	@staticmethod
	def get_backlogdir(root):
		return root + '/data/backlog/'
	@staticmethod
	def get_archivedir(root):
		return root + '/data/archives/'
	@staticmethod
	def get_arhive_filename(now):
		return now.strftime("%Y%m%d%H%M%S") + ".json"
	
	@staticmethod
	def daterange(start, end):
		dates = []
		for n in range((end - start).days):
			dates.append(start + timedelta(n))
		return dates
		
	@staticmethod
	def calculate_backlog(tickets, member, daterange):
		my_tickets = [t for t in tickets if t['reporter'] == member]    
		backlogs = {}
		for date in daterange:
			sum_point = sum([int(t['point']) for t in my_tickets if t.has_key('due_assign') and t['due_assign'] == date])
			backlogs[date] = str(sum_point)
		
		burndown = {}
		point = sum([int(v) for v in backlogs.values()])
		all_point = point
		for k,v in sorted(backlogs.items()):
			point -= int(v)
			burndown[k] = str(point)
			
		burndown['Start'] = str(all_point)
		return burndown