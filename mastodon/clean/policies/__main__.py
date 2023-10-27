import argparse
import pathlib

from multiprocessing.dummy import Pool as ThreadPool
from . import convert, Config, CONFIG

parser = argparse.ArgumentParser(__package__)

parser.add_argument('--all', action='store_true', default=False)
parser.add_argument('--threads', default=4)

args = parser.parse_args()

def process(filename):
    url = filename.parts[-2]
    date = filename.parts[-1].split('.')[0]
    doc = convert(filename)
    outdir = pathlib.Path(CONFIG.get_outdir(__package__))
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir.joinpath(f'{url}_{date}.txt')
    with open(outfile, 'w') as f:
        f.write(str(doc))

pool = ThreadPool(int(args.threads))
if args.all:
    pool.map(process, CONFIG.get_data_files('mastodon.fetch.policies'))