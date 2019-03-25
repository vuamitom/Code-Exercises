import requests
import time
import os
import datetime
from datetime import timedelta
import zipfile
import csv

# http://images1.cafef.vn/data/20190322/CafeF.SolieuGD.22032019.zip
url = 'http://images1.cafef.vn/data/__date1__/CafeF.SolieuGD.__date2__.zip'
output_dir = '/home/tamvm/Projects/stock_data'
unzip_dir = '/home/tamvm/Projects/stock_data/unzip'

def crawl_range(start_date, end_date, output_dir):
    """download zip file for range """
    day_count = (end_date - start_date).days + 1
    for d in [start_date + timedelta(days=n) for n in range(day_count)]:
        crawl(d, output_dir)
        time.sleep(5)

def crawl(date, output_dir):
    """download zip file for a certain date"""
    date_url = url.replace('__date2__', date.strftime('%d%m%Y')).replace('__date1__', date.strftime('%Y%m%d'))
    print('downloading ', date_url, '')
    r = requests.get(date_url)
    if r.status_code != requests.codes.ok:
        print('error: ', r.status_code)
        return
    with open (os.path.join(output_dir, os.path.basename(date_url)), 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

def unzip(d):
    """ unzip downloaded files"""
    for p in os.listdir(d):
        fn = os.path.join(d, p)
        # print(fn)
        if os.path.isfile(fn) and p.endswith('.zip'):
            print ('unzip ', fn)
            zip_ref = zipfile.ZipFile(fn, 'r')
            zip_ref.extractall(unzip_dir)
            zip_ref.close()

def merge_csv(d):
    """read all csv and put into a single file"""
    data = []
    for c in os.listdir(d):
        fn = os.path.join(d, c)
        if os.path.isfile(fn) and c.endswith('.csv'):
            with open(fn, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    data.append(row)
    return data


if __name__ == '__main__':
    n = datetime.datetime.now()
    start = n - timedelta(days=7)
    crawl_range(start, n, output_dir)
    unzip(output_dir)
    merge_csv(unzip_dir)