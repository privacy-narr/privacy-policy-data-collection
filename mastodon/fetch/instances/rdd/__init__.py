import requests, json, os
from datetime import datetime
from .... import CONFIG

default_extensions = [
        "social",
        "local",
        "space",
        "town",
        "club"
      ]
key_extensions = "extensions"

OUTDIR = CONFIG.get_outdir(__name__)
today = datetime.today()
OUTFILE_RAW = "{1}{0}{4}_{3:02d}_{2:02d}{0}serverlist.jsons".format(os.sep, OUTDIR, today.day, today.month, today.year)
existing_domains = set()

if os.path.exists(OUTFILE_RAW):
    with open(OUTFILE_RAW, 'r') as f:
        for i, line in enumerate(f.readlines(), start=1):
            instance = json.loads(line)
            domain = instance['domain'] if 'domain' in instance else ''
            if domain == '':
                print(f'Line {i} does not contain a domain name: {instance}')
            elif domain in existing_domains:
                # replace this with logging later
                print(f'Line {i} contains a repeat of domain {domain}')
            existing_domains.add(domain)
elif not os.path.exists(os.path.dirname(OUTFILE_RAW)):
    os.makedirs(os.path.dirname(OUTFILE_RAW))


def check_domain(domain):
    logfile = f'{today.year}_{today.month:02d}_{today.day:02d}.log'
    get_info = lambda version : requests.get(f'https://{domain}/api/{version}/instance', timeout=10, allow_redirects=True)
    r = None
    try:
        r = get_info('v2')
    except:
        try:
            # Now try the older endpoint?
            r = get_info('v1')
        except Exception as e:
            with open(logfile, 'a') as f:
                f.write(f'Unhandled exception for {domain}:{e}\n')
            return
    if r.ok:
        try:
            dat = r.json()
            # Since we allow redirects, record the original domain
            dat["rdd_request"] = domain
            with open(OUTFILE_RAW, 'a') as f:
                json.dump(dat, f)
                f.write('\n')
        except requests.exceptions.JSONDecodeError:
            with open(logfile, 'a') as f:
                f.write(f'Detected JSON error for {domain}\n')
