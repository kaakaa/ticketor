import urllib2
import json

class Trac:
	host = None
	port = None
	project_name = None

	jsonrpc_path = 'login/jsonrpc'
	ticket_path = 'ticket/%s'
	
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

		u = self.get_or_else(app, 'trac.rpc.username', 'admin')
		p = self.get_or_else(app, 'trac.rpc.password', 'admin')
		self.install_auth(u, p)
		
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
		req = urllib2.Request("http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.jsonrpc_path))
		req.add_header('Content-Type', 'application/json')
		return urllib2.urlopen(req, json.dumps(json_params)).read()

	def get_ticket_link(self, id):
		return "http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.ticket_path % id)
		
	def get_team_members(self):
		return self.members
	def get_milestones(self):
		return self.milestones
	def get_components(self):
		return self.components
