# Normalize policies
import argparse
import pathlib
import pypandoc
import re

from ... import Config, CONFIG

parser = argparse.ArgumentParser(__package__)
parser.add_argument('--threads', default=4)

class Doc():
    def __init__(self, txt):
        self.txt = txt

    def __or__(self, fn):
        return Doc(fn(self.txt))
    
    def __str__(self):
        return self.txt

# Luis' preprocessing functions (with some small modifications)

def removeServerNames(server_name:str, replace_with='<SERVER_NAME>'):
    """
        Removes and replaces the server name in the policy text with a different string.
    """
    return lambda policy_txt : policy_txt.replace(server_name, replace_with)


def lowerCasePolicyText(policy_txt:str):
    """
        Simply makes the whole text lower case.
    """
    return policy_txt.lower()

# Removed: subsumed by pandoc
# def removeFormatting(policy_txt:str):
#     regex = re.compile(r"(^:+(\s\{.*\})*)|(#+\s.*)|(\*)", re.MULTILINE)
#     return re.sub(regex, '', policy_txt)


# Edited -- previously replaced single newlines with empty string; now normalizes all 
# whitespace to be a single space character
def removeEmptyLines(policy_txt:str):
    return re.sub(r'\s+', ' ', policy_txt)

def removeHorizontalBar(policy_txt:str):
    # Replaces the horizontal bar. Does not replace singular hyphens, en-dashes, nor em-dashes
    return re.sub(r'----+', '', policy_txt)

def convert(filename: pathlib.PosixPath):
    if filename.parts[-1] == 'txt':
        print(filename)
        exit(1)
    file = pathlib.Path(filename)
    servername = file.parts[-2]
    return Doc(pypandoc.convert_file(file, 'plain')) \
            | removeServerNames(servername) \
            | lowerCasePolicyText \
            | removeHorizontalBar \
            | removeEmptyLines 
