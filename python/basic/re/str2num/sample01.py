# -*- coding: utf-8 -*-
import re

date = "2024年4月1日"

date2 = re.findall(r"\d+", date)

print(date2) # ['2024', '4', '1']