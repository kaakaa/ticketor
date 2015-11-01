import json
import urllib2

class SearchTicket:
	
    def make_params(self, forms):
        non_empty_forms = dict((k, v) for k, v in forms.items() if len(v) != 0)
        buf = []
        if "member" in non_empty_forms:
            buf.append("reporter=" + forms.get("member"))
        if "owner" in non_empty_forms:
            buf.append("owner=" + forms.get("owner"))
        if "component" in non_empty_forms:
            buf.append("component=" + forms.get("component"))
        if "milestone" in non_empty_forms:
            buf.append("milestone=" + forms.get("milestone"))
        if "due_assign" in non_empty_forms:
            buf.append("due_assign=" + forms.get("due_assign"))
        if "due_close" in non_empty_forms:
            buf.append("due_close=" + forms.get("due_close"))
        if "max" in non_empty_forms:
            buf.append("max=" + forms.get("max"))

        return {
            "params": [ "&".join(filter(None, buf))],
            "method": "ticket.query"
        }

    def format_response(self, response):
        res_json = json.loads(response)
        if res_json['error'] is None:
            return res_json['result']
        else:
            raise urllib2.HTTPError(url='http://trac', code=500, msg=res_json['error'], hdrs={}, fp=None)

    def search_ticket(self, trac, forms):
        json_params = self.make_params(forms)
        response = trac.callrpc(json_params)
        return self.format_response(response)

