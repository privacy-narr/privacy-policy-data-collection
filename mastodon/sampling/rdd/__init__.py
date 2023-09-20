import requests, json
from collections import defaultdict

codes = defaultdict(list)
not_mastodon = []
data = dict()
other_errors = []

def check_domain(domain):
    try:
        r = requests.get(f'https://{domain}/api/v2/instance', timeout=30, allow_redirects=True)
        codes[r.status_code].append(domain)
        if r.ok:
            try:
                dat = r.json()
                with open('mastodon_servers', 'a') as f:
                    json.dump(dat, f)
            except requests.exceptions.JSONDecodeError:
                with open('log', 'a') as f:
                    f.write(f'Detected JSON error for {domain}\n')
            except Exception as e:
                with open('log', 'a') as f:
                    f.write(f'Unhandled exception for {domain}:' + str(e))
    except requests.exceptions.ConnectionError:
        not_mastodon.extend(domain)
