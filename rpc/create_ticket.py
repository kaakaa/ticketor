import json
import os
import urllib2
from datetime import datetime
from bottle import HTTPResponse

class CreateTicket:
	
    def make_params(self, forms):
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

    def format_response(self, response):
        res_json = json.loads(response)
        if res_json['error'] is None:
            return res_json['result']
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def create_master_ticket(self, trac, forms):
        json_params = self.make_params(forms)
        response = trac.callrpc(json_params)
        return self.format_response(response)

    def create_slave_ticket(self, trac, forms, parent_id, member):
        json_params = self.make_params(forms)
        json_params['params'][2]['parents'] = str(parent_id)
        json_params['params'][2]['reporter'] = member
    
        response = trac.callrpc(json_params)
        return self.format_response(response)
    
    def create_team_ticket(self, trac, forms):
        ticket_id = self.create_master_ticket(trac, forms)
        
        for m in ['admin', 'guest']:
            ticket_id2 = self.create_slave_ticket(trac, forms, ticket_id, m)
        
        now = datetime.now()
        result = { "Date": now.strftime("%Y/%m/%d %H:%M:%S"), "Title": forms.get("title"), "Link": trac.get_ticket_link(ticket_id)}
        filename = now.strftime("%Y%m%d%H%M%S") + ".json"
        with open(os.path.abspath('./archives/' + filename), 'w') as fp:
            json.dump(result, fp)
        
        return HTTPResponse(status=200, body="Create ticket: %s" % ticket_id)
