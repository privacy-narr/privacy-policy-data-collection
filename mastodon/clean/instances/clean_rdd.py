#! /usr/bin/env python3
# De-duplicates and filters raw data. 
# Only selects servers where English is an official language

import json, os
from ... import CONFIG, Config

servers = {}

root = '{1}{0}data{0}mastodon{0}instances{0}rdd'.format(os.sep, CONFIG[Config._mastodon][Config._datarepo])

for folder in os.listdir(root):
    folder = root + os.sep + folder
    for filename in os.listdir(folder):
        with open(folder + os.sep + filename, 'r') as f:
            for line in f:
                data = json.loads(line)
                if 'domain' in data:
                    domain = data['domain']
                    if domain not in servers:
                        servers[domain] = data

with open(f'cleaned_data{os.sep}rdd_serverlist.jsons', 'w') as f:
    for instance in servers.values():
        json.dump(instance, f)
        f.write('\n')

print(len(servers), 'unique servers')