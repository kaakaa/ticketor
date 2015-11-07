import urllib2
import json
import gevent
from gevent import monkey

monkey.patch_all()


class Trac:
	host = None
	port = None
	project_name = None

	jsonrpc_path = 'login/jsonrpc'
	ticket_path = 'ticket/%s'
	
	auth = {}
	
	milestones = []
	components = []

	members = []
	
	def get_or_else(self, app, key, default):
		return app.config[key] if app.config.has_key(key) else default

	def initialize(self, app):
		self.host = self.get_or_else(app, 'trac.host', 'localhost')
		self.port = self.get_or_else(app, 'trac.port', '')
		self.port = '' if len(self.port) == 0 else ':' + self.port

		self.project_name = self.get_or_else(app, 'trac.project_name', 'SampleProject')
		self.members = self.get_or_else(app, 'trac.team_members', [])

		self.auth['user'] = self.get_or_else(app, 'trac.rpc.username', 'admin')
		self.auth['pass'] = self.get_or_else(app, 'trac.rpc.password', 'admin')
		
		self.milestones = self.read_milestones()
		self.components = self.read_components()

	def read_milestones(self):
		response = self.callrpc({ 'params': '', 'method': 'ticket.milestone.getAll' })
		return json.loads(response)['result']

	def read_components(self):
		response = self.callrpc({ 'params': '', 'method': 'ticket.component.getAll' })
		return json.loads(response)['result']

	def install_auth(self, user, password):
		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, '%s%s' % (self.host, self.port), user, password)
		authhandler = urllib2.HTTPDigestAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		
		urllib2.install_opener(opener)

	def callrpc(self, json_params):
		self.install_auth(self.auth['user'], self.auth['pass'])
		req = urllib2.Request("http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.jsonrpc_path))
		req.add_header('Content-Type', 'application/json')
		return urllib2.urlopen(req, json.dumps(json_params)).read()
		
	def request_par(self, id, json_params, buf):
		res = self.callrpc(json_params)
		res_dict = {'id': id, 'response': res}
		buf.append(res_dict)

	def callrpc_par(self, json_params_array):
		buf = []
		jobs = [gevent.spawn(self.request_par, id, json, buf) for id, json in json_params_array.items()]
		gevent.joinall(jobs)
		return buf

	def get_ticket_link(self, id):
		return "http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.ticket_path % id)
		
	def get_team_members(self):
		return self.members
	def get_milestones(self):
		return self.milestones
	def get_components(self):
		return self.components
	def get_trac_home(self):
		return  "http://%s%s/trac/%s" % (self.host, self.port, self.project_name)
	def get_kanban_home(self):
		return "http://%s%s/trac/%s/kanban" % (self.host, self.port, self.project_name)
