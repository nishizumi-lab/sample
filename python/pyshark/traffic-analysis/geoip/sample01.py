import pyshark
import geoip2.database
from collections import defaultdict
import ipaddress

# pcapファイルの読み込み
cap = pyshark.FileCapture('traffic.pcap', display_filter='ip')

# GeoLite2 データベースの読み込み
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

# 国別トラフィック量を記録する辞書
country_traffic = defaultdict(int)

for pkt in cap:
    try:
        dst_ip = pkt.ip.dst

        # プライベートIPかどうかを判定
        if ipaddress.ip_address(dst_ip).is_private:
            continue  # ローカルIPならスキップ

        # 国名を取得
        country = reader.country(dst_ip).country.name

        # パケットサイズ加算
        size = int(pkt.length)
        country_traffic[country] += size

    except Exception:
        continue  # IP層がない／不明なパケットなどを無視

## 結果を表示
for country, total_bytes in sorted(country_traffic.items(), key=lambda x: -x[1]):
    if country not in (None, "Unknown"):
        print(f"{country}: {total_bytes:,} bytes")

    
    
    