import trac
import json
import sys
import urllib2
from bottle import default_app, route, run, static_file, template, request, HTTPResponse

sys.path.append('rpc')
import create_ticket

app = default_app()
trac_server = trac.Trac()


## Static files 

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./public/js')

@route('/css/<filename>')
def css_static(filename):
    return static_file(filename, root='./public/css')

@route('/css/images/<filename>')
def css_static(filename):
    return static_file(filename, root='./public/css/images')

@route('/fonts/<filename>')
def fonts_static(filename):
    return static_file(filename, root='./public/fonts')

## REST Phage

@route('/form')
def index():
    return template('form', milestones=trac_server.get_milestones(), components=trac_server.get_components())

@route('/tasks')
def tasks():
    return template('tasks')

@route('/regist', method='post')
def regist():
    try:
        return create_ticket.CreateTicket().create_team_ticket(trac_server, request.forms)
    except urllib2.URLError, e:
        return HTTPResponse(status=e.code, body='The server couldn\'t fulfill the request. %s' % e.msg)

## Initialize Phase

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v)) 
        for k, v in dictionary.items())

def initialize():
    with open('./conf/config.json') as fp:
        app.config.load_dict(convert_keys_to_string(json.load(fp)))
    trac_server.initialize(app)

if __name__ == '__main__':
    initialize()
    run(host='localhost', port=8081, reloader=True)
