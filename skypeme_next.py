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
def get_result_email(link):
    table1=None
    try:
        while table1==None:
            r=requests.get(link)
            result1=BeautifulSoup(r.content)
            table1=result1.find('table')
            if not table1==None:
                break
            get_result_email(link)
    except Exception as e:
        print('Function Error')
        get_result_email(link)
    return table1
for index,Domain in input_data.itertuples():
    emails=[]
    count+=1
    domain=str(Domain.encode("utf-8")).lower()
    domain=domain.split('/')[0]
    print(str(count)+' '+domain)
    #Getting Result
    try:
        r = requests.get("http://www.skymem.info/srch",{'q': domain})
    except Exception as e:
        print(e)
    #Getting Link
    try:
        result=BeautifulSoup(r.content)
        next_link=result.find_all('a')[16].get('href')
        if not next_link.startswith( '/domain' ):
            continue
        nl='http://www.skymem.info'+next_link[:-1]
        #print(nl)
    except Exception as e:
        print('Result Error '+str(e))
        continue
    # Count Of Email Result
    try:
        email_count=result.find('div',{'title':'Domain related to this search result'})
        #print('email count tag found')
        #print(email_count)
        email_count=email_count.find('small').text.replace('(','').split()[0]
        email_count_h=int(email_count)/2
        email_page_count=email_count_h%5
        if email_page_count>0:
            email_count_h=(email_count_h-email_page_count)+5
        print('Email Result Count : '+str(email_count))
        print('Email Result Count Half : '+str(email_count_h))
        page_range=email_count_h/5
        if page_range>200:
            page_range=200
        print('Email Result Page Range: '+str(page_range))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    except Exception as e:
        print(e)
    for page_number in range(3,page_range+1,1):
        result_link=nl+str(page_number)
        #print(result_link)
        try:
            table1=get_result_email(result_link)  
            for aa in table1.find_all('a'):
                emails.append(aa.text)
        except Exception as e:
            print('Count Error '+str(e))
            print(str(table1))
    json1={domain:emails}
    #print(json1)
    try:
        with open(str(input_file)+'_output.json') as feedsjson:
            feeds = json.load(feedsjson)
        feeds.append(json1)
        with open(str(input_file)+'_output.json', mode='w') as f:
            f.write(json.dumps(feeds, indent=2))
    except Exception as e:
        print(e)
        
        
    
    
