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

	members = ['admin', 'guest']

	def initialize(self, app):
		self.host = app.config['trac.host'] if app.config.has_key('trac.host') else 'localhost'
		self.port = app.config['trac.port'] if app.config.has_key('trac.port') else '8080'
		self.project_name = app.config['trac.project_name'] if app.config.has_key('trac.project_name') else 'SampleProject'
		self.members = app.config['trac.team_members'] if app.config.has_key('trac.team_members') else ['admin']

		u = app.config['trac.rpc.username'] if app.config.has_key('trac.rpc.username') else 'admin'
		p = app.config['trac.rpc.password'] if app.config.has_key('trac.rpc.password') else 'admin'
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
		passman.add_password(None, '%s:%s' % (self.host, self.port), user, password)
		authhandler = urllib2.HTTPDigestAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		
		urllib2.install_opener(opener)


	def callrpc(self, json_params):
		req = urllib2.Request("http://%s:%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.jsonrpc_path))
		req.add_header('Content-Type', 'application/json')
		return urllib2.urlopen(req, json.dumps(json_params)).read()

	def get_milestones(self):
		return self.milestones
	def get_components(self):
		return self.components
