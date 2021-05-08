import pandas as pd
import numpy as np
from pprint import pprint
import apache_log_parser

import pathlib
import csv

def load_csv_data(csv_path):
    data_csv = pathlib.Path(csv_path)
    datas = []

    with data_csv.open('r', encoding='cp932', newline='') as f:
        h = next(csv.reader(f))
        for c in csv.reader(f):
            # リストに追加
            datas.append(c)

    return datas

def read_apache_log(log_path, logformat='%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'):
    parser = apache_log_parser.make_parser(logformat)
    dst = []
    dst_error = []
    with open(log_path) as f:
        for line in f:
            try:
                parsed_line = parser(line)
                dst.append(parsed_line)
            except ValueError:
                dst_error.append(line)


    return dst

log_path = "C:/github/sample/python/squid/00_sample_data/access.log"
csv_path = 'C:/github/sample/python/squid/00_sample_data/access.csv'

df = pd.DataFrame(read_apache_log(log_path))
#df['time_received'] = df['time_received'].str[1:]
#df['time_received'] = df['time_received'].str[:-1]

df.drop(columns=['time_received','time_received_isoformat','time_received_tz_datetimeobj','time_received_tz_isoformat','time_received_utc_datetimeobj','time_received_utc_isoformat'])
df['id']= df.index
#df.to_csv()

#datas = load_csv_data(csv_path)

print(df.values.tolist())
