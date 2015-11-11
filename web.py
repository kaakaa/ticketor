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

trac_server = trac.Trac()
app = default_app()
BaseTemplate.defaults['get_trac_home'] = trac_server.get_trac_home
BaseTemplate.defaults['get_kanban_home'] = trac_server.get_kanban_home
BaseTemplate.defaults['get_team_members'] = trac_server.get_team_members
BaseTemplate.defaults['get_milestones'] = trac_server.get_milestones
BaseTemplate.defaults['get_components'] = trac_server.get_components
 
@error(500)
def custom500(error):
    return tob(template('error', message=error.traceback))

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
@view('form')
def form():
    return {}

@route('/update')
@view('update')
def update():
    return dict(tickets = [])

@route('/api/search', method='post')
def api_search():
    from tracrpc import SearchTicket
    import get_ticket
    
    ticket_ids = SearchTicket.execute(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)
    
    response.status = 200
    response.content_type = 'application/json'
    return {'result': dict(tickets = sorted(tickets, key=lambda t: t.get('id')))}

@route('/search', method='post')
@view('update')
def view_search():
    body = api_search()['result']
    response.content_type = 'text/html; charset=UTF-8'
    return body

@route('/update', method='post')
@view('update')
def update():
    import update_ticket
    
    tickets = update_ticket.UpdateTicket().update_ticket(trac_server, request.forms)
    return dict(tickets = sorted(tickets, key=lambda t: t.get('id')))

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

def read_backlogs(backlog, member):
    result = []
    with open(backlog, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == member:
                buf = []
                for e in row:
                    if e.isdigit():
                        buf.append(int(e))
                    else:
                        buf.append(e)
                result.append(buf)
    return result

@route('/api/backlogs', method='post')
def api_backlogs():
    ms = request.forms.get('milestone', '_')
    member = request.forms.get('member', '_')
    data = []
    
    backlog = Helper.get_backlog(rootdir, ms + '_estimated.csv')
    if os.path.exists(backlog):
        header = read_backlogs(backlog, 'Date')
        data += header
        burndown = read_backlogs(backlog, member)[0]
        burndown[0] = 'Estimated'
        data.append(burndown)
    
    backlog = Helper.get_backlog(rootdir, ms + '_actual.csv')
    if os.path.exists(backlog):
        burndown = read_backlogs(backlog, member)[0]
        burndown[0] = 'Actual'
        data.append(burndown)
    
    response.status = 200
    response.content_type = 'application/json'
    return {'result': data}


@route('/backlog', method='post')
def backlog():
    # Report Ticket
    from tracrpc import SearchTicket
    import get_ticket
    
    ticket_ids = SearchTicket.execute(trac_server, request.forms)
    tickets = get_ticket.GetTicket().get_ticket(trac_server, ticket_ids)

    start = datetime.strptime(request.forms.get('start', '2000/01/01'), '%Y/%m/%d')
    end = datetime.strptime(request.forms.get('end', '2000/01/02'), '%Y/%m/%d')

    dates = Helper.daterange(start, end)
    header = ['Date', 'Start'] + dates
    result = []
    for member in trac_server.get_team_members():
        backlogs = Helper.calculate_data(tickets, member, dates)
        result.append(backlogs)
        
    # Calculate All Member's burndown
    all_member = [str(sum([int(per_member[daily]) for per_member in result])) for daily in range(1, len(result[0]))]
    all_member.insert(0, 'ALL')
    result.append(all_member)
    
    result.insert(0, header)
    file = Helper.get_backlog(rootdir, request.forms.get('milestone', 'none') + '_estimated.csv')
    with open(file, 'w') as fp:
        for col in result:
            fp.write(','.join(col))
            fp.write('\n')

    # Closing Ticket
    import changelog_ticket
    change_ticket = changelog_ticket.ChangeLogTicket().get_changelog(trac_server, ticket_ids)
    close_burndown = []
    for member in trac_server.get_team_members():
        owned_logs = [t for t in change_ticket if t.has_key('member') and t['member'] == member]
        closed_ticket = []
        for ol in owned_logs:
            t = next((t for t in tickets if ol['id'] == t['id']), None)
            if t is not None:
                t['closed'] = ol['datetime']
                closed_ticket.append(t)
        close_burndown.append(Helper.calculate_data_actual(closed_ticket, member, dates, next((r for r in result if r[0] == member))[1]))

    # Calculate All Member's burndown
    all_member = [str(sum([int(per_member[daily]) for per_member in close_burndown])) for daily in range(1, len(close_burndown[0]))]
    all_member.insert(0, 'ALL')
    close_burndown.append(all_member)
    
    close_burndown.insert(0, header)
    file = Helper.get_backlog(rootdir, request.forms.get('milestone', 'none') + '_actual.csv')
    with open(file, 'w') as fp:
        for col in close_burndown:
            fp.write(','.join(col))
            fp.write('\n')

    redirect('/burndown')
    
@route('/burndown')
@view('burndown')
def burn():
    response.content_type = 'text/html; charset=UTF-8'
    return dict(data=[])

@route('/burndown', method='post')
@view('burndown')
def burndown():
    body = api_backlogs()['result']
    response.content_type = 'text/html; charset=UTF-8'
    return dict(data=body, member = request.forms.get('member', '_'))

@route('/regist', method='post')
def regist():
    from tracrpc import CreateTicket
    try:
        ticket_id = CreateTicket.create_team_ticket(trac_server, request.forms)

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
