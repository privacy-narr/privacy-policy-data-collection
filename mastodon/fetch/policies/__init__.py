import csv, json, os, requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ... import CONFIG 

# Grab the policies for the input path

FORMATS=['jsons', 'tsv', 'csv', 'txt']
today = datetime.today()

def extract_policy(url):
    OUTDIR = CONFIG.get_outdir(__name__) + os.sep + url
    OUT = "{1}{0}{4}_{3:02d}_{2:02d}".format(os.sep, OUTDIR, today.day, today.month, today.year)
    ERR = f'pp_fetch_failures_{today.year}_{today.month:02d}_{today.day:02d}.err'
    if os.path.exists(OUT): return 
    try:
        resp = requests.get(f'https://{url}', allow_redirects=True, timeout=10)
        if not resp.ok:
            with open(ERR, 'a') as f:
                f.write(f'GET failed on https://{url}:\t{str(resp)}\n')
                return    
        pp_url = f'https://{url}/privacy-policy'
        resp = requests.get(pp_url, allow_redirects=True, timeout=10)
        if not resp.ok:
            with open(ERR, 'a') as f:
                f.write(f'GET failed on {pp_url}:\t{str(resp)}\n')
                return
        options = Options()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(pp_url)
        except Exception as e:
            with open(ERR, 'a') as f:
                f.write(f'GET failure from headless Chrome for {pp_url}:\t{str(e)}')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        pp = soup.find('div', {'class' : 'privacy-policy'})
        os.makedirs(OUTDIR, exist_ok=True)
        with open(OUT+'.html', 'w') as f:
            if pp:
                f.write(str(pp))
            else:
                f.write(str(soup.contents))
    except Exception as e:
        with open(ERR, 'a') as f:
            f.write(f'Uncaught exception for {url}:\t{str(e)}\n')


def get_servernames(filepath, format):
    with open(filepath, 'r') as f:
        if format == 'jsons':
            return [json.loads(obj)['domain'].strip() for obj in f.readlines()]
        elif format in ['tsv', 'csv']:
            sniffer = csv.Sniffer()
            sample = f.read(1024)
            headersp = sniffer.has_header(sample)
            dialect = sniffer.sniff(sample)
            f.seek(0)
            reader = csv.reader(f, dialect=dialect)
            if headersp:
                headers = reader.__next__()
                print(headers)
                url_index = headers.index('domain')
            else:
                url_index = 1
            return [row[url_index].strip() for row in reader]
        elif format == 'txt':
            return [domain.strip() for domain in f.readlines()]
        else:
            raise ValueError(f'Format not yet implemented: {format}')
                
