import requests, json, os
from collections import defaultdict
from datetime import datetime
from ... import CONFIG

codes = defaultdict(list)
not_mastodon = []
data = dict()
other_errors = []

OUTDIR = CONFIG.get_outdir(__name__)
today = datetime.today()
OUTFILE_RAW = "{1}{0}{4}_{3:02d}_{2:02d}{0}serverlist.jsonl".format(os.sep, OUTDIR, today.day, today.month, today.year)
existing_domains = set()

if os.path.exists(OUTFILE_RAW):
    with open(OUTFILE_RAW, 'r') as f:
        for i, line in enumerate(f.readlines(), start=1):
            instance = json.loads(line)
            domain = instance['domain']
            if domain in existing_domains:
                # replace this with logging later
                print(f'Line {i} contains a repeat of domain {domain}')
            existing_domains.add(domain)
elif not os.path.exists(os.path.dirname(OUTFILE_RAW)):
    os.makedirs(os.path.dirname(OUTFILE_RAW))


def check_domain(domain):
    try:
        r = requests.get(f'https://{domain}/api/v2/instance', timeout=30, allow_redirects=True)
        codes[r.status_code].append(domain)
        if r.ok:
            try:
                dat = r.json()
                with open(OUTFILE_RAW, 'a') as f:
                    json.dump(dat, f)
                    f.write('\n')
            except requests.exceptions.JSONDecodeError:
                with open('log', 'a') as f:
                    f.write(f'Detected JSON error for {domain}\n')
    except Exception as e:
        with open('log', 'a') as f:
            f.write(f'Unhandled exception for {domain}:' + str(e))