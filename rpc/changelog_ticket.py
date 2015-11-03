import json
import urllib2
from datetime import datetime

class ChangeLogTicket:
    def make_params(self, id):
        return {
            "params": [ int(id) ],
            "method": "ticket.changeLog"
        }

    def format_response(self, res_dict):
        id = res_dict['id']
        response = res_dict['response']
        res_json = json.loads(response)
        if res_json['error'] is None:
            result = res_json['result']
            close_logs = [{'id': id, 'datetime': datetime.strftime(datetime.strptime(r[0][u"__jsonclass__"][1], '%Y-%m-%dT%H:%M:%S'), '%Y/%m/%d'), 'member': r[1]} for r in result if r[2] == 'status' and r[4] == 'closed']
            recent = {}
            if close_logs != []:
                recent = sorted(close_logs, key=lambda l: l['datetime'], reverse=True)[0]
            return recent
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def get_changelog(self, trac, ids):
        json_params_array = {}
        for id in ids:
            json_params_array[id] = (self.make_params(id))
        
        tickets = trac.callrpc_par(json_params_array)
        return [self.format_response(res_dict) for res_dict in tickets]

