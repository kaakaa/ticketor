import json
import urllib2

class GetTicket:
	
    def make_params(self, id):
        return {
            "params": [ int(id) ],
            "method": "ticket.get"
        }

    def format_response(self, response):
        res_json = json.loads(response)
        if res_json['error'] is None:
            return res_json['result']
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def get_ticket(self, trac, ids):
        tickets = []
        for id in ids:
            json_params = self.make_params(id)
            response = trac.callrpc(json_params)
            ticket = self.format_response(response)[3]
            ticket[u'id'] = id
            tickets.append(ticket)
            
        return tickets

