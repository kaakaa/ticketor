import trac
import json
import urllib2
from bottle import route, run, static_file, template, request, HTTPResponse

trac = trac.Trac()
members = ['admin', 'guest']

def make_params(forms):
    title = forms.get('title')
    desc = forms.get('desc')
    point = forms.get('point')
    component = forms.get('component')
    milestone = forms.get('milestone')
    due_assign = forms.get('due_assign')
    due_close = forms.get('due_close')
    
    return {
        'params': 
            [
                title, 
                desc, 
                {
                    'component': component,
                    'milestone': milestone,
                    'point': point,
                    'due_assign': due_assign,
                    'due_close': due_close
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
    print json_params
    response = trac.callrpc(json_params)
    return format_response(response)

def create_slave_ticket(forms, parent_id, member):
    json_params = make_params(forms)
    json_params['params'][2]['parents'] = str(parent_id)
    json_params['params'][2]['reporter'] = member
    
    response = trac.callrpc(json_params)
    return format_response(response)

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



@route('/form')
def index():
    return template('form', milestones=trac.get_milestones(), components=trac.get_components())

@route('/tasks')
def tasks():
    return template('tasks')

@route('/regist', method='post')
def regist():
    try:
        ticket_id = create_master_ticket(trac, request.forms)
        
        for m in members:
            ticket_id2 = create_slave_ticket(request.forms, ticket_id, m)
            print ticket_id2        
        
        return HTTPResponse(status=200, body="Create ticket: %s" % ticket_id)

    except urllib2.URLError, e:
        return HTTPResponse(status=e.code, body='The server couldn\'t fulfill the request. %s' % e.msg)

run(host='localhost', port=8081, reloader=True)
