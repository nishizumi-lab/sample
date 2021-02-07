var test = function() {

    console.log(ipToLong('192.168.1.254')); // 3232236030
    console.log(ipToLong('192.168.1.256')); // false
    console.log(longToIp(3232236030)); // 192.168.1.254   
    console.log(longToIp(3232236029)); // 192.168.1.253  
    console.log(longToIp(255)); // 0.0.0.255
    console.log(longToIp(256)); // 0.0.1.0
    console.log(nwAdress('192.168.1.254', '255.255.255.0')); // 192.168.1.0
    console.log(cidrToSubnetmask(24)); // 255.255.255.0
    console.log(subnetmaskToCidr("255.255.255.0")); // 24
}
  