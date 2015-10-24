import trac
import json
import urllib2
from bottle import route, run, template, request, HTTPResponse

trac = trac.Trac()
members = ['admin', 'guest']

def make_params(forms):
    title = forms.get('title')
    desc = forms.get('desc')
    point = forms.get('point')
    
    return {
        'params': 
            [
                title, 
                desc, 
                {
                    'milestone': 'Iterate1',
                    'point': point,
                    'due_start': '2015/10/27'
                }
            ],
        'method': 'ticket.create'
    }

def format_response(response):
    res_json = json.loads(response)
    if res_json['error'] is None:
        return res_json['result']
    else:
        raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

def create_master_ticket(trac, forms):
    json_params = make_params(forms)
    response = trac.callrpc(json_params)
    return format_response(response)

def create_slave_ticket(forms, parent_id, member):
    json_params = make_params(forms)
    json_params['params'][2]['parents'] = str(parent_id)
    json_params['params'][2]['reporter'] = member
    
    response = trac.callrpc(json_params)
    return format_response(response)

@route('/form')
def index():
    return template('form')

@route('/regist', method='post')
def regist():
    try:
        trac.install_auth('admin', 'admin')
        ticket_id = create_master_ticket(trac, request.forms)
        
        for m in members:
            ticket_id2 = create_slave_ticket(request.forms, ticket_id, m)
            print ticket_id2        
        
        return HTTPResponse(status=200, body="Create ticket: %s" % ticket_id)

    except urllib2.URLError, e:
        return HTTPResponse(status=e.code, body='The server couldn\'t fulfill the request. %s' % e.msg)
    
run(host='localhost', port=8081, reloader=True)
