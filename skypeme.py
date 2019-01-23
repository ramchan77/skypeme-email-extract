import re
import pandas as pd
import time
import glob
import string
import json
import requests
import justext
from bs4 import BeautifulSoup

csv_files=glob.glob('*.csv')
input_file=string.replace(csv_files[0], '.csv', '')
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
with open(str(input_file)+'_output.json', 'w') as outfile:
    json.dump([], outfile)

for index,Domain in input_data.itertuples():
    count+=1
    domain=str(Domain.encode("utf-8")).lower()
    domain=domain.split('/')[0]
    print(str(count)+' '+domain)
    try:
        r = requests.get("http://www.skymem.info/srch",{'q': domain})
    except Exception as e:
        print(e)
    try:
        result=BeautifulSoup(r.content)
        table=result.find('table')
        emails=[]
        for aa in table.find_all('a'):
            emails.append(aa.text)
        json1={domain:emails}
    except Exception as e:
        print(e)
    try:
        with open(str(input_file)+'_output.json') as feedsjson:
            feeds = json.load(feedsjson)
        feeds.append(json1)
        with open(str(input_file)+'_output.json', mode='w') as f:
            f.write(json.dumps(feeds, indent=2))
    except Exception as e:
        print(e)
        
        
    
    
