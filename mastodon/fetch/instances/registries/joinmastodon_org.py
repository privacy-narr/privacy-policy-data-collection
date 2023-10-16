import json
import requests

from . import make_dump_path

dump_path = make_dump_path(__name__, "mastodon-server-dump.jsonl")

r = requests.get('https://api.joinmastodon.org/servers', timeout=30)

if r.ok:
    obj = r.json()
    with open(dump_path, 'a') as f:
        json.dump(obj, f)
    
