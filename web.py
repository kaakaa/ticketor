import trac
import json,csv
import glob
import os, sys
import urllib2
from datetime import datetime, timedelta
from bottle import *
from helper import Helper

rootdir = os.path.abspath('.')
TEMPLATE_PATH.insert(0, os.path.abspath('./views'))

sys.path.append('rpc')


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

@route('/api/search', method='post')
def api_search():
    import search_ticket
    import get_ticket
    
    ticket_ids = search_ticket.SearchTicket().search_ticket(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)
    
    response.status = 200
    response.content_type = 'application/json'
    return {'result': dict(members = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = sorted(tickets, key=lambda t: t.get('id')))}

@route('/search', method='post')
@view('update')
def view_search():
    body = api_search()['result']
    response.content_type = 'text/html; charset=UTF-8'
    return body

@route('/update', method='post')
def update():
    import update_ticket
    
    tickets = update_ticket.UpdateTicket().update_ticket(trac_server, request.forms)
    return template('update',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = sorted(tickets, key=lambda t: t.get('id')))
    

@route('/api/archives')
def api_archives():
    files = sorted(glob.glob(rootdir + '/data/archives/*.json'), reverse=True)
    def read_json(file):
        with open(file) as fp:
            return json.load(fp)
    body = map(read_json, [f for f in files[0:10]])
    response.status = 200
    response.content_type = 'application/json'
    return {'result': body}
    
@route('/archives')
@view('archives')
def archives():
    body = api_archives()['result']
    response.content_type = 'text/html; charset=UTF-8'
    return dict(archives=body)

@route('/api/backlogs', method='post')
def api_backlogs():
    ms = request.forms.get('milestone', '_')
    data = []
    backlog = Helper.get_backlog(rootdir, ms + '.csv')
    if os.path.exists(backlog):
        with open(backlog, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
               buf = []
               for e in row:
                   if e.isdigit():
                       buf.append(int(e))
                   else:
                       buf.append(e)
               data.append(buf)
               
    response.status = 200
    response.content_type = 'application/json'
    return {'result': data}

@route('/backlog', method='post')
def backlog():
    import search_ticket
    import get_ticket
    
    ticket_ids = search_ticket.SearchTicket().search_ticket(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)

    start = datetime.strptime(request.forms.get('start', '2000/01/01'), '%Y/%m/%d')
    end = datetime.strptime(request.forms.get('end', '2000/01/02'), '%Y/%m/%d')

    dates = Helper.daterange(start, end)
    result = []
    for member in trac_server.get_team_members():
        backlogs = Helper.calculate_burndown(tickets, member, dates)
        result.append(backlogs)
        
    dates.insert(0, 'Date')
    dates.insert(1, 'Start')
    
    result.insert(0, dates)
    
    file = Helper.get_backlog(rootdir, request.forms.get('milestone', 'none') + '.csv')
    with open(file, 'w') as fp:
        for col in result:
            fp.write(','.join(col))
            fp.write('\n')
    redirect('/burndown')
    
@route('/burndown')
@view('burndown')
def burn():
    response.content_type = 'text/html; charset=UTF-8'
    return dict(data=[], milestones = trac_server.get_milestones())

@route('/burndown', method='post')
@view('burndown')
def burndown():
    body = api_backlogs()['result']
    response.content_type = 'text/html; charset=UTF-8'
    return dict(data=body, milestones = trac_server.get_milestones())


@route('/regist', method='post')
def regist():
    import create_ticket
    try:
        ticket_id = create_ticket.CreateTicket().create_team_ticket(trac_server, request.forms)

        # Output archive file
        now = datetime.now()
        result = { "Date": now.strftime("%Y/%m/%d %H:%M:%S"), "Title": str(request.forms.get("title")), "Link": trac_server.get_ticket_link(ticket_id)}
        with open(os.path.abspath(Helper.get_archivedir(rootdir) + Helper.get_archive_filename(now)), 'w') as fp:
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
