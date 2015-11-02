from datetime import timedelta

class Helper:
	@staticmethod
	def get_backlogdir(root):
		return root + '/data/backlog/'
		
	@staticmethod
	def daterange(start, end):
		dates = []
		for n in range((end - start).days):
			dates.append(start + timedelta(n))
		return dates