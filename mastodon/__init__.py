import os

if os.path.exists('./mastodon/.data-repo'):
    with open('./mastodon/.data-repo', 'r') as f:
        DATAREPO = f.read()
else:
    raise ValueError('Data repository location not set. Please run `python -m mastodon` from the top level of this repository to initialize.')