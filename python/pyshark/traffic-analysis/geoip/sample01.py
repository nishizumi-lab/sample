import pyshark
import geoip2.database
from collections import defaultdict
import ipaddress

# pcapファイルの読み込み
cap = pyshark.FileCapture('D:/github/nishizumi/zabbix/python/test-data/traffic.pcap', display_filter='ip')

# GeoLite2 データベースの読み込み
reader = geoip2.database.Reader('D:/github/nishizumi/zabbix/python/test-data/GeoLite2-Country.mmdb')

# 辞書初期化
send_traffic = defaultdict(int)           # グローバル送信
recv_traffic = defaultdict(int)           # グローバル受信
local_traffic_by_dst = defaultdict(int)   # ローカル宛先ごとの受信トラフィック
local_traffic_by_src = defaultdict(int)   # ローカル送信元ごとの送信トラフィック ←🆕

for pkt in cap:
    try:
        src_ip = pkt.ip.src
        dst_ip = pkt.ip.dst
        size = int(pkt.length)

        src_ip_obj = ipaddress.ip_address(src_ip)
        dst_ip_obj = ipaddress.ip_address(dst_ip)

        # 🌐 グローバル送受信の集計
        if not src_ip_obj.is_private and not src_ip_obj.is_loopback:
            try:
                src_country = reader.country(src_ip).country.name
                if src_country:
                    send_traffic[src_country] += size
            except:
                pass

        if not dst_ip_obj.is_private and not dst_ip_obj.is_loopback:
            try:
                dst_country = reader.country(dst_ip).country.name
                if dst_country:
                    recv_traffic[dst_country] += size
            except:
                pass

        # 🏠 ローカルIPに関する集計（送信元・宛先）
        if dst_ip_obj.is_private or dst_ip_obj.is_loopback:
            local_traffic_by_dst[dst_ip] += size

        if src_ip_obj.is_private or src_ip_obj.is_loopback:
            local_traffic_by_src[src_ip] += size

    except AttributeError:
        continue

# 結果表示

print("\n📤 国別送信トラフィック:")
for country, total_bytes in sorted(send_traffic.items(), key=lambda x: -x[1]):
    print(f"{country}: {total_bytes:,} bytes")

print("\n📥 国別受信トラフィック:")
for country, total_bytes in sorted(recv_traffic.items(), key=lambda x: -x[1]):
    print(f"{country}: {total_bytes:,} bytes")

print("\n🏠 ローカルアドレス別受信トラフィック（宛先IP）:")
for dst_ip, total_bytes in sorted(local_traffic_by_dst.items(), key=lambda x: -x[1]):
    print(f"{dst_ip} : {total_bytes:,} bytes")

print("\n🚀 ローカルアドレス別送信トラフィック（送信元IP）:")
for src_ip, total_bytes in sorted(local_traffic_by_src.items(), key=lambda x: -x[1]):
    print(f"{src_ip} : {total_bytes:,} bytes")
 