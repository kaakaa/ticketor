# -*- coding: utf-8 -*-

import urllib2
import json
import gevent
from gevent import monkey
from datetime import datetime

monkey.patch_all()

class Trac:
	"""Tracの情報を保持し、Tracとのインタフェースとなるクラス"""
	
	loading_at = None
	"""Tracの設定をロードした日時"""

	host = None
	"""TracのIP"""
	port = None
	"""Tracのポート番号。ポート指定が不要の場合、空文字列を設定する。"""
	project_name = None
	"""Tracプロジェクト名"""
	team_name = None
	"""チーム名。バーンダウンチャートのタイトルに使用される。"""

	jsonrpc_path = 'login/jsonrpc'
	"""TracRPCのURLの一部"""
	ticket_path = 'ticket/%s'
	"""TracチケットリンクのURLの一部"""
	
	auth = {"user": "", "pass": ""}
	"""Trac認証情報"""
	
	milestones = []
	"""Tracのマイルストーン一覧"""
	components = []
	"""Tracのコンポーネント一覧"""

	members = []
	"""configファイルで指定したTracユーザ一覧"""
	
	def get_or_else(self, app, key, default):
		"""app.configにキー key が存在する場合はそのvalueを、キー keyが存在しない場合はdefaultを返す
		
		:param app: 辞書
		:param key: キー値
		:param default: app.configにキー値 keyが存在しない場合に返される値
		"""
		return app.config[key] if app.config.has_key(key) else default

	def initialize(self, app):
		"""Tracクラスの初期設定を行う（必須）
		
		:param app: configファイルの内容を保持したbottle.pyアプリケーションオブジェクト
		"""
		
		self.loading_at = datetime.now()
		
		self.host = self.get_or_else(app, 'trac.host', 'localhost')
		self.port = self.get_or_else(app, 'trac.port', '')
		self.port = '' if len(self.port) == 0 else ':' + self.port

		self.project_name = self.get_or_else(app, 'trac.project_name', 'SampleProject')
		self.team_name = self.get_or_else(app, 'trac.team_name', '')
		self.members = self.get_or_else(app, 'trac.team_members', [])

		self.auth['user'] = self.get_or_else(app, 'trac.rpc.username', 'admin')
		self.auth['pass'] = self.get_or_else(app, 'trac.rpc.password', 'admin')
		
		self.milestones = self.read_milestones()
		self.components = self.read_components()

	def read_milestones(self):
		"""Tracに登録されているマイルストーン一覧を取得する"""
		response = self.callrpc({ 'params': '', 'method': 'ticket.milestone.getAll' })
		return json.loads(response)['result']

	def read_components(self):
		"""Tracに登録されているコンポーネント一覧を取得する"""
		response = self.callrpc({ 'params': '', 'method': 'ticket.component.getAll' })
		return json.loads(response)['result']

	def install_auth(self, user, password):
		"""TracRPCのDigest認証をurllib2に設定する
		
		:param user: TracユーザーID
		:param password: userに対するパスワード
		"""
		passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
		passman.add_password(None, '%s%s' % (self.host, self.port), user, password)
		authhandler = urllib2.HTTPDigestAuthHandler(passman)
		opener = urllib2.build_opener(authhandler)
		
		urllib2.install_opener(opener)

	def callrpc(self, json_params):
		"""TracRPCを実行する
		
		configより読みこんだ情報から、TracRPCへDigest認証をセットしたリクエストを送信し、
		responseを返します。
		
		:param json_params: Trac JSON RPCのリクエストパラメータ(dict)
		"""
		self.install_auth(self.auth['user'], self.auth['pass'])
		req = urllib2.Request("http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.jsonrpc_path))
		req.add_header('Content-Type', 'application/json')
		return urllib2.urlopen(req, json.dumps(json_params)).read()
		
	def request_par(self, id, json_params, buf):
		"""TracRPCのresponseにチケットIDを付与した結果をbufferに格納する
		
		geventによる並列処理でTracRPCを実行した場合、そのresponseを直接取得できないため、
		bufferに格納していく。
		
		:param id: TracチケットID
		:param json_params: Trac JSON RPCのリクエストパラメータ(dict)
		:param buf: TracRPC結果格納buffer
		"""
		res = self.callrpc(json_params)
		res_dict = {'id': id, 'response': res}
		buf.append(res_dict)

	def callrpc_par(self, json_params_array):
		"""TracRPCを並列に実行する
		
		configより読みこんだ情報から、TracRPCへDigest認証をセットしたリクエストを並列で送信し、
		responseを返します。
		
		:param json_params_array: Trac JSON RPCのリクエストパラメータ配列
		"""
		buf = []
		jobs = [gevent.spawn(self.request_par, id, json, buf) for id, json in json_params_array.items()]
		gevent.joinall(jobs)
		return buf

	def get_ticket_link(self, id):
		"""引数のチケットIDのチケットページリンクを生成する
		
		:pram id: TracチケットID
		"""
		return "http://%s%s/trac/%s/%s" % (self.host, self.port, self.project_name, self.ticket_path % id)
		
	def get_team_members(self):
		"""configファイルで指定したTracユーザ一覧を返す"""
		return self.members
	def get_milestones(self):
		"""Tracのマイルストーン一覧を返す"""
		return self.milestones
	def get_components(self):
		"""Tracのコンポーネント一覧を返す"""
		return self.components
	def get_trac_home(self):
		"""TracのURLを返す"""
		return  "http://%s%s/trac/%s" % (self.host, self.port, self.project_name)
	def get_kanban_home(self):
		"""TracのカンバンページのURLを返す"""
		return "http://%s%s/trac/wiki/%s/kanban" % (self.host, self.port, self.project_name)
	def get_team_name(self):
		"""configファイルで指定したチーム名を返す"""
		return self.team_name

	def connection_test(self):
		"""Tracへのコネクションテスト"""
		response = self.callrpc({ 'params': '', 'method': 'system.getAPIVersion' })
		return json.loads(response)['error']

	def get_trac_settings(self):
		"""Tracプロジェクトの設定を返す"""
		return {
			'loading_at': self.loading_at.strftime('%Y/%m/%d %H:%M:%S'),
			'host': self.host,
			'port': self.port,
			'project_name': self.project_name,
			'team_name': self.team_name,
			'auth': self.auth,
			'milestones': self.milestones,
			'components': self.components,
			'members': self.members
		}
