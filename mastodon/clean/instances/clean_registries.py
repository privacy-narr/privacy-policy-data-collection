#! /usr/bin/env python3
# De-duplicates and filters raw data. 
# Only selects servers where English is an official language

import json, os
from . import Instance
from ... import Config, CONFIG

english_servers     = set()
no_language_servers = set()
nonenglish_servers  = set()

root = '{1}{0}data{0}mastodon{0}instances{0}registries'.format(os.sep, CONFIG[Config._mastodon][Config._datarepo])


for registry in os.listdir(root):
    reg = registry
    registry = root + os.sep + registry
    for folder in os.listdir(registry):
        folder = registry + os.sep + folder
        for filename in os.listdir(folder):
            with open(folder + os.sep + filename, 'r') as f:
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
                        

                            
with open(f'.{os.sep}cleaned_data{os.sep}registries_serverlist.csv', 'w') as f:
    f.write('\t'.join(Instance.headers) + '\n')
    for instance in english_servers:
        f.write(str(instance))

print(len(nonenglish_servers), "non-english servers")
print(len(no_language_servers), "servers with no language information")
print(len(english_servers), 'english servers')