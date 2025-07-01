import pyshark
import geoip2.database
from collections import defaultdict

cap = pyshark.FileCapture('traffic.pcap', display_filter='ip')

reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
country_traffic = defaultdict(int)

for pkt in cap:
    if 'IP' in pkt:
        ip = pkt.ip.dst
        try:
            country = reader.country(ip).country.name
        except:
            country = "Unknown"
        size = int(pkt.length)
        country_traffic[country] += size

for country, total_bytes in country_traffic.items():
    print(f"{country}: {total_bytes} bytes")