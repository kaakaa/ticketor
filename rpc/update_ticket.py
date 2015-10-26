import json
import urllib2

class UpdateTicket:
	
    def make_params(self, id, status, user):
        return {
            "params": [
                int(id),
                "Bulk status update",
                {
                    "status": status,
                    "owner": user
                }
            ],
            "method": "ticket.update"
        }

    def format_response(self, response):
        res_json = json.loads(response)
        if res_json['error'] is None:
            return res_json['result']
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def update_ticket(self, trac, forms):
        user = forms.get('targetuser')
        status = forms.get('status')
        tickets = []
        for id in forms.getall('ticketid'):
            json_params = self.make_params(id, status, user)
            response = trac.callrpc(json_params)
            ticket = self.format_response(response)[3]
            ticket[u'id'] = id
            tickets.append(ticket)
            
        return tickets

