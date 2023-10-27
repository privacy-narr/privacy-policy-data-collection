#! /usr/bin/env python3
# De-duplicates and filters raw data. 
# Only selects servers where English is an official language

import json, os, pathlib
from .. import Instance
from .... import Config, CONFIG

english_servers     = set()
no_language_servers = set()
nonenglish_servers  = set()

DATA_REPO = pathlib.Path(CONFIG[Config._mastodon][Config._datarepo])
root = DATA_REPO.joinpath('data', *__package__.replace('clean', 'fetch').split('.'))



for registry in root.iterdir():
    reg = registry.parts[-1]
    for folder in registry.iterdir():
        for filename in folder.iterdir():
            with open(filename, 'r') as f:
                for line in f:
                    datalist = json.loads(line)
                    for instance in datalist:
                        if 'language' in instance:
                            if instance['language'] == 'en':
                                english_servers.add(Instance(reg, instance))
                            elif 'languages' in instance:
                                if 'en' in instance['languages']:
                                    english_servers.add(Instance(reg, instance))
                            else:
                                nonenglish_servers.add(Instance(reg, instance))
                        elif 'languages' in instance:
                            if instance['languages'] and 'en' in instance['languages']:
                                english_servers.add(Instance(reg, instance))
                            else:
                                nonenglish_servers.add(Instance(reg, instance))
                        else:
                            no_language_servers.add(Instance(reg, instance))
                        

parent_dir = DATA_REPO.joinpath('data', *__package__.split('.'))
parent_dir.mkdir(parents=True, exist_ok=True)
                            
with open(parent_dir.joinpath('serverlist.csv'), 'w') as f:
    f.write('\t'.join(Instance.headers) + '\n')
    for instance in english_servers:
        f.write(str(instance))

print(len(nonenglish_servers), "non-english servers")
print(len(no_language_servers), "servers with no language information")
print(len(english_servers), 'english servers')