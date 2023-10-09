import argparse
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool
from . import check_domain, OUTFILE_RAW
from ... import CONFIG, Config

print(Config._mastodon)

DATAREPO = CONFIG[Config._mastodon][Config._datarepo]

parser = argparse.ArgumentParser(description="A program that generates a csv of contact information for confirmed Mastodon instances using a list of words as input")
parser.add_argument('--extensions', nargs='+', default=['social', 'local', 'space', 'town', 'club'], help='The extensions that should be appended to the input words to test whether the server at the generated domain is running Mastodon.')
parser.add_argument('--nthreads', default=1, help='The number of threads to use. Default is 1.', type=int)
parser.add_argument('words', help='The file that contains the words/strings to be used for the base of the domain.')
parser.add_argument('--exclusions', nargs='+', default=[], help='A list of files containing instance domains to exclude.')


args = parser.parse_args()
exclusions = set()

# switch to data frames later
# first single threaded mode

with open(args.words, 'r') as f:
    words = [w.strip() for w in f.readlines()]

for filename in args.exclusions:
    possible_formats = ['${DATAREPO}', 'DATAREPO']
    for fmt in possible_formats:
        if fmt in filename:
            filename = filename.replace(fmt, DATAREPO)
            break
    with open(filename, 'r') as f:
        for domain in f.readlines():
            domain = domain.strip()
            if domain in exclusions:
                raise ValueError('Exclusion set contains duplicates:', domain)
            exclusions.add(domain)

def instance(word, ext):
    return f'{word}.{ext}'

domains = []
for word in words:
    for ext in args.extensions:
        d = instance(word, ext)
        if d in exclusions:
            print(f'{d} already contacted')
        else:
            domains.append(d)

print('Checking {} domains ({}, {}, ..., {}) and writing to {}'.format(len(domains), domains[0], domains[1], domains[-1], OUTFILE_RAW))

progress_bar = tqdm(total=len(domains))

def f(d):
    check_domain(d)
    progress_bar.update()

pool = ThreadPool(args.nthreads)
pool.map(f, domains)