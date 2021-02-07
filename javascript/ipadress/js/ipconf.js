var ipToBin = function(ipAdress) {
  return ipAdress.split(".").map(e => Number(e).toString(2).padStart(8, '0')).join('');
}

var ipToLong = function(ipAdress) {
  return parseInt(ipToBin(ipAdress), 2);
}

var longToIp = function(num) {
  let bin = Number(num).toString(2).padStart(32, '0')
  return [
      bin.slice(0, 8),
      bin.slice(8, 16),
      bin.slice(16, 24),
      bin.slice(24, 32),
  ].map(e => parseInt(e, 2)).join('.')
}

var cidrToSubnetmask = function(cidr) {
  return longToIp(parseInt(String("").padStart(cidr, '1').padEnd(32, '0'), 2));
}

var subnetmaskToCidr = function(subnetmask) {
  return ipToBin(subnetmask).split('1').length - 1;
}

var calcNetworkAdress = function(ipAdress, subnetMask) {
  return longToIp((ipToLong(ipAdress) & ipToLong(subnetMask)) >>> 0) ;
}

var calcBroadcastAdress = function(ipAdress, subnetMask) {
  return longToIp((ipToLong(ipAdress) | ~ ipToLong(subnetMask)) >>> 0);
}

var calcIpClass = function(ipAdress) {

  if (ipToLong("10.0.0.0") <= ipToLong(ipAdress) && ipToLong(ipAdress) <= ipToLong("10.255.255.255")) {
      return 'A'
  }
  if (ipToLong("172.16.0.0") <= ipToLong(ipAdress) && ipToLong(ipAdress) <= ipToLong("172.31.255.255")) {
      return 'B'
  }
  if (ipToLong("192.168.0.0") <= ipToLong(ipAdress) && ipToLong(ipAdress) <= ipToLong("192.168.255.255")) {
      return 'C'
  }
  return false;
}

// 同じネットワークアドレス内の先頭IPアドレス(ネットワークアドレス+1)
var calcIpStart = function(ipAdress, subnetMask) {
  return longToIp((ipToLong(ipAdress) & ipToLong(subnetMask)) + 1 >>> 0 ) ;
}

// 同じネットワークアドレス内の終端IPアドレス(ブロードキャストアドレス-1)
var calcIpEnd = function(ipAdress, subnetMask) {
  return longToIp((ipToLong(ipAdress) | ~ ipToLong(subnetMask)) -1  >>> 0);
}

// アドレス数
var calcAdressNum = function(ipAdress, subnetMask) {
  return ipToLong(calcBroadcastAdress(ipAdress, subnetMask)) - ipToLong(calcNetworkAdress(ipAdress, subnetMask)) + 1;
}

// ホストアドレス数 
var calcHostNum = function(ipAdress, subnetMask) {
  return ipToLong(calcBroadcastAdress(ipAdress, subnetMask)) - ipToLong(calcNetworkAdress(ipAdress, subnetMask)) - 1;
}