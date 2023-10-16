#! /usr/bin/env python
"""
  Authors: Luis Garcia, Emma Tosch
  Description: 
    Finds and extracts privacy policy text from servers listed on `mastodon-server-list.json`.
    Dumps content into a folder passed through a CLI argument.
"""

import argparse, re, sys
from argparse import ArgumentParser, Namespace
from multiprocessing.dummy import Pool as ThreadPool
from typing import *
from . import extract_policy, get_servernames, FORMATS
from ... import CONFIG, Config


class ConfigReplace(argparse.Action):
    
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None) -> None:
        # replace config variables in string
        assert type(values) is str
        match = re.match('%(.*?)%', values)
        if match is None: return 
        if len(match.groups()) == 1:
            key = match.group(1)
            if key.lower() in CONFIG[Config._mastodon]:
                replacement = CONFIG[Config._mastodon][key.lower()]
                new_value = values.replace(f'%{key}%', replacement)
                setattr(namespace, self.dest, new_value)
            else:
                raise ValueError(f'Key {key} not in configuration object; possible keys:\n', '\n\t'.join(CONFIG.__dict__.keys()))
        if 'format' not in namespace:
            ext = values.split('.')[-1]
            setattr(namespace, 'format', ext)


class FormatInfer(argparse.Action):
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None) -> None:
        print('calilng format infer')
        if values is None and 'filename' in namespace and namespace['filename']:
            ext = namespace['filename'].split('.')[-1]
            setattr(namespace, self.dest, ext)

parser = argparse.ArgumentParser(__package__, description='Fetches policies given the request. See usage for how to request.')
parser.add_argument('--filename', default=None, required=False, action=ConfigReplace)
parser.add_argument('--method', default=None)
parser.add_argument('--format', required=False, default=None, choices=FORMATS, action=FormatInfer)
parser.add_argument('--latest', default=True)
parser.add_argument('--threads', default=4)

args = parser.parse_args()


# resolve format
if not args.format:
    if args.filename:
        ext = args.filename.split('.')[-1].lower()
        if ext not in FORMATS:
            raise ValueError(f'Unrecognized format: {ext}')
        else:
            args.format = ext

if not args.filename:
    if args.method:
        method_data_dir = CONFIG.get_outdir('instances.rdd')
        print(method_data_dir)


if len(sys.argv) < 2:
    parser.print_help()


server_list = get_servernames(args.filename, args.format)
pool = ThreadPool(int(args.threads))
pool.map(extract_policy, server_list)