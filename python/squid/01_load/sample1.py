import pandas as pd
import numpy as np
import apache_log_parser
from pprint import pprint

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

log_path = "/Users/github/sample/python/squid/00_sample_data/access.log"
 
df = pd.DataFrame(read_apache_log(log_path))
df.to_csv('Users/github/sample/python/squid/00_sample_data/access.csv')
