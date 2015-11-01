import trac
import json,csv
import glob
import os, sys
import urllib2
from datetime import datetime, timedelta
from bottle import default_app, redirect, route, run, static_file, template, request, HTTPResponse, TEMPLATE_PATH

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


@route('/search', method='post')
def search():
    import search_ticket
    import get_ticket
    
    ticket_ids = search_ticket.SearchTicket().search_ticket(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)

    return template('update',
        members    = trac_server.get_team_members(),
        milestones = trac_server.get_milestones(),
        components = trac_server.get_components(),
        tickets    = sorted(tickets, key=lambda t: t.get('id')))
        
@route('/update', method='post')
def update():
    import update_ticket
    
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
def burn():
    return template('burndown', 
        data=[],
        milestones = trac_server.get_milestones())

@route('/burndown', method='post')
def burndown():
    ms = request.forms.get('milestone', '_')
    
    data = []
    backlog = rootdir + '/data/backlog/' + ms + '.csv'
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
    return template('burndown', 
        data=data,
        milestones = trac_server.get_milestones())

def daterange(start, end):
    dates = []
    for n in range((end - start).days):
        dates.append(start + timedelta(n))
    return dates

def calculate_backlog(tickets, member, daterange):
    my_tickets = [t for t in tickets if t['reporter'] == member]    
    backlogs = {}
    for date in daterange:
        sum_point = sum([int(t['point']) for t in my_tickets if t.has_key('due_assign') and t['due_assign'] == date])
        backlogs[date] = str(sum_point)
    
    burndown = {}
    point = sum([int(v) for v in backlogs.values()])
    all_point = point
    for k,v in sorted(backlogs.items()):
        point -= int(v)
        burndown[k] = str(point)
    burndown['Start'] = str(all_point)
    return burndown
        
@route('/backlog', method='post')
def backlog():
    import search_ticket
    import get_ticket
    
    ticket_ids = search_ticket.SearchTicket().search_ticket(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)
    
    start = datetime.strptime(request.forms.get('start', '2015/10/20'), '%Y/%m/%d')
    end = datetime.strptime(request.forms.get('end', '2015/10/31'), '%Y/%m/%d')

    dates = map(lambda d: d.strftime('%Y/%m/%d'), daterange(start, end))
    result = []
    for member in trac_server.get_team_members():
        backlogs = calculate_backlog(tickets, member, dates)
        backlogs_csv = [member, backlogs['Start']]
        for d in sorted(dates):
            backlogs_csv.append(backlogs[d])
        result.append(backlogs_csv)
        
    dates.insert(0, 'Date')
    dates.insert(1, 'Start')
    
    result.insert(0, dates)
    
    file = rootdir + '/data/backlog/' + request.forms.get('milestone', 'none') + '.csv'
    with open(file, 'w') as fp:
        for col in result:
            fp.write(','.join(col))
            fp.write('\n')
    redirect('/burndown')


@route('/regist', method='post')
def regist():
    import create_ticket
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
