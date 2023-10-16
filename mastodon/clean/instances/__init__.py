import requests, importlib, sys

class Instance():

    headers = ['registry', 'url', 'open', 'users', 'active_users', 'email']

    def __init__(self, registry, obj):
        self.registry = registry
        self.url      = {
            'joinmastodon_org' : lambda : obj['domain'],
            'instances_social' : lambda : obj['name'] 
        }[registry]()
        self.open     = {
            'instances_social' : lambda : obj['open_registrations'],
            'joinmastodon_org' : lambda : obj['approval_required']
        }[registry]()
        self.users = {
            'instances_social' : lambda : obj['users'],
            'joinmastodon_org' : lambda : obj['total_users']
        }[registry]()
        self.active_users = {
            'instances_social' : lambda : obj['active_users'],
            'joinmastodon_org' : lambda : obj['last_week_users']
        }[registry]()
        self.email = self._getemail(registry, obj)

    
    def _getemail(self, registry, obj):
        if registry == 'instances_social': 
            return obj['email']
        else:
            r = requests.get(f'https://{self.url}/api/v2/instance')
            try:
                r = r.json()
            except:
                try:
                    r = requests.get(f'https://{self.url}/api/v1/instance')
                    r = r.json()
                except:
                    print('instances data request failed for', self.url)
                    return ""
            if 'contact' in r:
                if 'email' in r['contact']:
                    return r['contact']['email']
            return ""
        
    def __str__(self):
        return f'{self.registry}\t{self.url}\t{self.open}\t{self.users}\t{self.active_users}\t{self.email}\n'
    
    def __eq__(self, other):
        return self.url == other.url
    
    def __hash__(self):
        return self.url.__hash__()
    


importlib.import_module(sys.argv[1], package=__name__)