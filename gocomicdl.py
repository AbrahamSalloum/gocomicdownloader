import datetime
import os
import requests
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }

# Config
base_url = 'https://www.gocomics.com/{}/{}/{}/{}'
comic_name = 'cathy'
save_dir = './comics/'+comic_name
first_date = '1976-11-22'
last_date="2010-10-04"
requestWaitMs = 500  # will be banned if this is to low

# Init Save Dir
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

file_list = sorted(os.listdir(save_dir))
file_count = len(file_list)

date_cursor = datetime.strptime(first_date, '%Y-%m-%d').date()
last_date = datetime.strptime(last_date, '%Y-%m-%d').date()

if file_count != 0: # this sucks, but it works
    last_file_name = os.path.basename(file_list[len(file_list) - 1])
    date_cursor =  datetime.strptime(os.path.splitext(last_file_name)[0],'%Y-%m-%d').date()
    print("Starting from checkpoint: {}".format(date_cursor))

while date_cursor <= last_date:
    save_file_name = '{}.gif'.format(date_cursor)
    print("Saving: {}".format(save_file_name))
    url = base_url.format(comic_name,date_cursor.year,date_cursor.month,date_cursor.day)
    r = requests.get(url, allow_redirects=True, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    comicdiv = soup.find_all("div", attrs={"data-shareable-model" : "FeatureItem"}) #find comic div(s)
    for comic in comicdiv:
        imgr = requests.get(comic['data-image'], allow_redirects=True, headers=headers)
        with open('{}/{}'.format(save_dir, save_file_name), 'wb') as fh:
            fh.write(imgr.content)

    nextdatebutton = soup.find_all("a", attrs={"class": re.compile(r'fa-caret-right')}) #find next comic in calendar
    print(nextdatebutton[0]["href"])
    url_date = '/{}/%Y/%m/%d'.format(comic_name)
    date_cursor = datetime.strptime(nextdatebutton[0]["href"], url_date).date()
    time.sleep(requestWaitMs / 1000)
