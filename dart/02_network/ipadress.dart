class Ip {
  Ip() {}
  String ipToBin(String ip) {
    // IP -> 4分割 -> 各要素を8ビットの2進数に変換して結合
    return ip.split(".").map((e) => int.parse(e).toRadixString(2).padLeft(8, '0')).toList().join('');
  } 

  int ipToLong(String ip) {
    return int.parse(ipToBin(ip), radix:2);
  }

  String longToIp(int ipLong) {
    String ipBin = ipLong.toRadixString(2).padLeft(32, '0');

    return [
        int.parse(ipBin.substring(0, 8), radix:2).toString(),
        int.parse(ipBin.substring(8, 16), radix:2).toString(),
        int.parse(ipBin.substring(16, 24), radix:2).toString(),
        int.parse(ipBin.substring(24, 32), radix:2).toString(),
    ].join('.');
  }

  String cidrTosubnet(int cidr) {
    return longToIp(int.parse("".padLeft(cidr, '1').padRight(32, '0'), radix:2));
  }


  int subnetToCidr(String subnet) {
    return ipToBin(subnet).split('1').length - 1;
  }

  String getNetworkAdress(String ip, String subnet) {
    return longToIp((ipToLong(ip) & ipToLong(subnet))) ;
  }

  String getBroadcastAdress(String ip, String subnet) {

    return longToIp(ipToLong(ip) | (ipToLong(subnet) ^ ipToLong('255.255.255.255')));
  }

  String getIpClass(String ip) {

    if (ipToLong("10.0.0.0") <= ipToLong(ip) && ipToLong(ip) <= ipToLong("10.255.255.255")) {
        return 'A';
    }
    if (ipToLong("172.16.0.0") <= ipToLong(ip) && ipToLong(ip) <= ipToLong("172.31.255.255")) {
        return 'B';
    }
    if (ipToLong("192.168.0.0") <= ipToLong(ip) && ipToLong(ip) <= ipToLong("192.168.255.255")) {
        return 'C';
    }
    return 'valid';
  }

  // 同じネットワークアドレス内の先頭IPアドレス(ネットワークアドレス+1)
  String getIpStart(String ip, String subnet) {
    return longToIp((ipToLong(ip) & ipToLong(subnet)) + 1) ;
  }

  // 同じネットワークアドレス内の終端IPアドレス(ブロードキャストアドレス-1)
  String getIpEnd(String ip, String subnet) {
    return longToIp((ipToLong(ip) | (ipToLong(subnet) ^ ipToLong('255.255.255.255')) )- 1);
  }

  // アドレス数
  int getAdressNum(String ip, String subnet) {
    return ipToLong(getBroadcastAdress(ip, subnet)) - ipToLong(getNetworkAdress(ip, subnet)) + 1;
  }

  // ホストアドレス数 
  int getHostNum(String ip, String subnet) {
    return ipToLong(getBroadcastAdress(ip, subnet)) - ipToLong(getNetworkAdress(ip, subnet)) - 1;
  }

}

void main() {
    var ip = Ip();
    print(ip.ipToBin('192.168.1.1')); // 11000000101010000000000100000001
    print(ip.ipToLong('0.0.0.1'));    // 1
    print(ip.longToIp(100));          // 0.0.0.100
    print(ip.cidrTosubnet(24));   // 255.255.255.0
    print(ip.subnetToCidr("255.255.255.0")); // 24
    print(ip.getNetworkAdress('192.168.1.1', '255.255.255.254')); // 192.168.1.0
    print(ip.getBroadcastAdress('192.168.1.1', '255.255.255.0')); // 192.168.1.255
    print(ip.getIpClass('192.168.1.1')); // C
    print(ip.getIpStart('192.168.1.100', '255.255.255.0')); // 192.168.1.1
    print(ip.getIpEnd('192.168.1.1', '255.255.255.0')); // 192.168.1.255
    print(ip.getAdressNum('192.168.1.1', '255.255.255.0')); // 256
    print(ip.getHostNum('192.168.1.100', '255.255.255.0')); // 254
}