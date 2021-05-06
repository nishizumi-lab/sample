import pandas as pd
import numpy as np
from datetime import datetime
import pytz

def parse_str(x):
    return x[1:-1]

def parse_datetime(x):
    dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))

df = pd.read_csv(
    'C:/github/sample/python/squid/00_sample_data/access.log',
    sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
    engine='python',
    na_values='-',
    header=None,
    usecols=[0, 4, 6, 7, 8, 9, 10],
    names=['ip', 'time', 'response_time', 'request', 'status', 'size', 'user_agent'],
    converters={'time': parse_datetime,
                'response_time': int,
                'request': parse_str,
                'status': int,
                'size': int,
                'user_agent': parse_str})