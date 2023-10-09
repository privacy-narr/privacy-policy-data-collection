import os 

from argparse import ArgumentParser
from datetime import datetime

from ... import CONFIG, Config

# Create a shared parser.
parser = ArgumentParser()

if Config._registries not in CONFIG[Config._mastodon]:
    with CONFIG:
        CONFIG[Config._mastodon][Config._registries] = {}

today = datetime.today()

def make_dump_path(name, fname):
    dir = "{1}{0}{2:02d}{3:02d}{4}{0}".format(os.sep, CONFIG.get_outdir(name), today.day, today.month, today.year)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + fname
