import json
import urllib2

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
        
        for m in trac.get_team_members():
            ticket_id2 = self.create_slave_ticket(trac, forms, ticket_id, m)
        
        return ticket_id

