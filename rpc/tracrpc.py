import json
import urllib2

class _TracRPC:
	@classmethod
	def make_params():
		return {'method': 'system.getAPIVersion'}
	
	@classmethod
	def format_response(cls, response):
		res_json = json.loads(response)
		if res_json['error'] is None:
			return res_json['result']
		else:
			raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)
	
	@classmethod
	def execute(cls, trac, forms):
		json_params = cls.make_params(forms)
		response = trac.callrpc(json_params)
		return cls.format_response(response)

class CreateTicket(_TracRPC):
	@classmethod
	def make_params(cls, forms):
		title = forms.get('title')
		desc = forms.get('desc')
		point = forms.get('point')
		component = forms.get('component')
		milestone = forms.get('milestone')
		due_assign = forms.get('due_assign')
		due_close = forms.get('due_close')
		
		return {
			'params': 
				[
					title, 
					desc, 
					{
						'component': component,
						'milestone': milestone,
						'point': point,
						'due_assign': due_assign,
						'due_close': due_close
					}
				],
			'method': 'ticket.create'
		}
	
	@classmethod
	def create_master_ticket(cls, trac, forms):
		json_params = cls.make_params(forms)
		response = trac.callrpc(json_params)
		return cls.format_response(response)
		
	@classmethod
	def create_slave_ticket(cls, trac, forms, parent_id, member):
		json_params = cls.make_params(forms)
		json_params['params'][2]['parents'] = str(parent_id)
		json_params['params'][2]['reporter'] = member
		
		response = trac.callrpc(json_params)
		return cls.format_response(response)
		
	@classmethod
	def create_team_ticket(cls, trac, forms):
		ticket_id = cls.create_master_ticket(trac, forms)
		
		for m in trac.get_team_members():
			ticket_id2 = cls.create_slave_ticket(trac, forms, ticket_id, m)
		
		return ticket_id



class SearchTicket(_TracRPC):
	@classmethod
	def make_params(cls, forms):
		non_empty_forms = dict((k, v) for k, v in forms.items() if len(v) != 0)
		buf = []
		if "member" in non_empty_forms:
			buf.append("reporter=" + forms.get("member"))
		if "owner" in non_empty_forms:
			buf.append("owner=" + forms.get("owner"))
		if "component" in non_empty_forms:
			buf.append("component=" + forms.get("component"))
		if "milestone" in non_empty_forms:
			buf.append("milestone=" + forms.get("milestone"))
		if "due_assign" in non_empty_forms:
			buf.append("due_assign=" + forms.get("due_assign"))
		if "due_close" in non_empty_forms:
			buf.append("due_close=" + forms.get("due_close"))
		if "max" in non_empty_forms:
			buf.append("max=" + forms.get("max"))

		return {
			"params": [ "&".join(filter(None, buf))],
			"method": "ticket.query"
		}

	@classmethod
	def execute(cls, trac, forms):
		json_params = cls.make_params(forms)
		response = trac.callrpc(json_params)
		return cls.format_response(response)

