import trac
import json
import glob
import os, sys
import urllib2
from datetime import datetime
from bottle import default_app, redirect, route, run, static_file, template, request, HTTPResponse, TEMPLATE_PATH
#from bottledaemon import daemon_run

rootdir = os.path.abspath('.')
TEMPLATE_PATH.insert(0, os.path.abspath('./views'))

sys.path.append('rpc')
import create_ticket
import search_ticket
import get_ticket
import update_ticket

app = default_app()
trac_server = trac.Trac()


## Static files 

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root=rootdir+'/public/js')

@route('/css/<filename>')
def css_static(filename):
    return static_file(filename, root=rootdir+'/public/css')

@route('/css/images/<filename>')
def css_static(filename):
    return static_file(filename, root=rootdir+'/public/css/images')

@route('/fonts/<filename>')
def fonts_static(filename):
    return static_file(filename, root=rootdir+'/public/fonts')

## REST Phage

@route('/')
def index():
    redirect('/form')

@route('/form')
def form():
    return template('form',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components())

@route('/update')
def update():
    return template('update',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = [])


@route('/search', method='post')
def search():
    ticket_ids = search_ticket.SearchTicket().search_ticket(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)

    return template('update',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = sorted(tickets, key=lambda t: t.get('id')))
        
@route('/update', method='post')
def update():
    tickets = update_ticket.UpdateTicket().update_ticket(trac_server, request.forms)
    return template('update',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = sorted(tickets, key=lambda t: t.get('id')))
    
def read_json(file):
    with open(file) as fp:
        return json.load(fp)

@route('/archives')
def archives():
    files = sorted(glob.glob(rootdir + '/data/archives/*.json'), reverse=True)
    archives = map(read_json, [f for f in files[0:10]])
    return template('archives', archives=archives)

@route('/burndown')
def burndown():
    return template('burndown')

@route('/regist', method='post')
def regist():
    try:
        ticket_id = create_ticket.CreateTicket().create_team_ticket(trac_server, request.forms)

        # Output archive file
        now = datetime.now()
        result = { "Date": now.strftime("%Y/%m/%d %H:%M:%S"), "Title": str(request.forms.get("title")), "Link": trac_server.get_ticket_link(ticket_id)}
        filename = now.strftime("%Y%m%d%H%M%S") + ".json"
        with open(os.path.abspath(rootdir + '/data/archives/' + filename), 'w') as fp:
            json.dump(result, fp)
        
        redirect('/archives', 303)
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
    with open(rootdir + '/conf/config.json') as fp:
        app.config.load_dict(convert_keys_to_string(json.load(fp)))
    trac_server.initialize(app)

if __name__ == '__main__':
    initialize()
    run(host="0.0.0.0", port="8081")
    # daemon_run(host='0.0.0.0', port="5200", pidfile=(rootdir + '/daemon/bottle.pid'), logfile=(rootdir + '/daemon/bottle.log'))
