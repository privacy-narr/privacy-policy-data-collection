#! /usr/bin/env python
"""
  Author: Luis Garcia
  Description:
    Fetches server data using the API described in https://instances.social/api/doc/#api-_ 
    Configured by the .env file that should be in the same directory as this project.
"""

import json
import os
import pathlib
import requests
import time 

from argparse import ArgumentParser
from collections import defaultdict
from ... import get_outdir, MASTODON, __registries

__FETCH_SERVER_FIELDS_TO_KEEP = "FETCH_SERVER_FIELDS_TO_KEEP"
__default_FETCH_SERVER_FIELDS_TO_KEEP = "id,name,up,users,open_registrations,info.topic,info.categories,info.languages,active_users,email,admin".split(",")
__FETCH_SERVER_API_ENDPOINT = "FETCH_SERVER_API_ENDPOINT"
__default_FETCH_SERVER_API_ENDPOINT = "instances/list"
__FETCH_SERVER_API_AUTH_TOKEN = "FETCH_SERVER_API_AUTH_TOKEN"


file_dir = pathlib.Path(__file__).parent.resolve()
dump_path = get_outdir(__name__) + os.sep + 'mastodon-server-dump.jsonl'

if __registries__ not in MASTODON:
  MASTODON[__registries__] = {}

if 
  fields_to_keep = os.environ['FETCH_SERVER_FIELDS_TO_KEEP'].split(',')
print('Parsing out the fields to keep:', os.environ['FETCH_SERVER_FIELDS_TO_KEEP'])


if os.path.exists(dump_path):
  os.remove(dump_path)

arg_parser = ArgumentParser()
arg_parser.add_argument('--pagesize', type=int, help='Amount of items to retrieve per API call. Default: 100', default=100)
args = arg_parser.parse_args()

api_host = 'https://instances.social/api/1.0'
api_server_endpoint = os.environ['FETCH_SERVER_API_ENDPOINT']

next_id = None
result_count = 0

while True:
  res = requests.get(
    f'{api_host}/{api_server_endpoint}',
    params={
      'count': args.pagesize,
      'min_id': next_id 
    },
    headers={
      'Authorization': f"Bearer {os.environ['FETCH_SERVER_API_AUTH_TOKEN']}"
    }
    ).json()
    
  if 'error' in res.keys():
    raise Exception(res['error'])
  
  if 'next_id' in res['pagination']:
    next_id = res['pagination']['next_id']
  else:
    next_id = None
  
  result_count += len(res['instances'])
  print('Amount results:', result_count)
  
  parsed_results = []
  # Parse out fields according to the FETCH_SERVER_FIELDS_TO_KEEP environment variable
  for instance in res['instances']:
    parsed_instance = defaultdict()
    
    # If the field has the dotted notation, then it is
    # a path in an object hierarchy to follow.
    # Otherwise, just grab the field.
    for field in fields_to_keep:
      if '.' in field:
        path = field.split('.')
        child_key = path[-1]
        
        # Walk down the path
        data = instance
        for p in path:
          data = data[p]
          
        parsed_instance[child_key] = data
        
      else:
        parsed_instance[field] = instance[field]
        
    parsed_results.append(parsed_instance)
  
  # Dump the json into a json list file.
  with open(dump_path, 'a') as server_list_file:
    server_list_file.write(json.dumps(parsed_results)+'\n')
    
  if not bool(next_id):
    break
  
  # Sleep for 1 sec to avoid getting marked as a bot
  time.sleep(1)
    
  
