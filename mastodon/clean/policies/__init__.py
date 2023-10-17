# Run pandoc on all of the html policies
import argparse
import subprocess
from ... import Config, CONFIG

parser = argparse.ArgumentParser(__package__)
parser.add_argument('--threads', default=4)

def run_pandoc(): pass