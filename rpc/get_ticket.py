import json
import urllib2

class GetTicket:
	
    def make_params(self, id):
        return {
            "params": [ int(id) ],
            "method": "ticket.get"
        }

    def format_response(self, res_dict):
        id = res_dict['id']
        response = res_dict['response']
        res_json = json.loads(response)
        if res_json['error'] is None:
            result = res_json['result'][3]
            result[u'id'] = id
            return result
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def get_ticket(self, trac, ids):
        json_params_array = {}
        for id in ids:
            json_params_array[id] = (self.make_params(id))
        
        tickets = trac.callrpc_par(json_params_array)
        return [self.format_response(res_dict) for res_dict in tickets]

