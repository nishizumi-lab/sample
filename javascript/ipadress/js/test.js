var test = function() {

    console.log(ipToBin('192.168.1.254')); // 11000000101010000000000111111110 
    console.log(ipToLong('192.168.1.254')); // 3232236030
    console.log(longToIp(3232236030)); // 192.168.1.254   
    console.log(longToIp(3232236029)); // 192.168.1.253  
    console.log(longToIp(255)); // 0.0.0.255
    console.log(longToIp(256)); // 0.0.1.0
    console.log(cidrToSubnetmask(24)); // 255.255.255.0
    console.log(subnetmaskToCidr("255.255.255.0")); // 24
    console.log(calcNetworkAdress('192.168.1.254', '255.255.255.0')); // 192.168.1.0
    console.log(calcBroadcastAdress('192.168.1.254', '255.255.255.0')); // 192.168.1.255
    console.log(calcIpClass('192.168.1.254')); // C
    console.log(calcIpStart('192.168.1.254', '255.255.255.0')); // 192.168.1.1
    console.log(calcIpEnd('192.168.1.254', '255.255.255.0')); // 192.168.1.254
    console.log(calcAdressNum('192.168.1.254', '255.255.255.0')); // 256
    console.log(calcHostNum('192.168.1.254', '255.255.255.0')); // 254
}