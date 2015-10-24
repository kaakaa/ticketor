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
	
	def __init__(self, host = 'localhost', port = '8080', project_name = 'SampleProject'):
		self.host = host
		self.port = port
		self.project_name = project_name

		self.install_auth('admin', 'admin')
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
