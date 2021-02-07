var ipToLong = function(ipAdress) {
  var i = 0;
  // Allows decimal, octal, and hexadecimal ipAdress components.
  // Allows between 1 (e.g. 127) to 4 (e.g 127.0.0.1) components.
  // 10進数、8進数、16進数のipAdressコンポーネントを許可
  // 1（例：127）から4（例：127.0.0.1）のコンポーネントを許可
  ipAdress = ipAdress.match(
    /^([1-9]\d*|0[0-7]*|0x[\da-f]+)(?:\.([1-9]\d*|0[0-7]*|0x[\da-f]+))?(?:\.([1-9]\d*|0[0-7]*|0x[\da-f]+))?(?:\.([1-9]\d*|0[0-7]*|0x[\da-f]+))?$/i
  ); 
  // Verify ipAdress format.
  // IPアドレスの形式を満たしているか検証
  if (!ipAdress) {
    // Invalid format.
    return false;
  }
  // Reuse ipAdress variable for component counter.
  // コンポーネントカウンターにipAdress変数を使用します。
  ipAdress[0] = 0;
  for (i = 1; i < 5; i += 1) {
    ipAdress[0] += !!((ipAdress[i] || '')
      .length);
    ipAdress[i] = parseInt(ipAdress[i]) || 0;
  }

  // Continue to use ipAdress for overflow values.
  // does not allow any component to overflow.
  // オーバーフロー値に引き続きipAdressを使用します。
  // コンポーネントのオーバーフローを許可しません。
  ipAdress.push(256, 256, 256, 256);
  // Recalculate overflow of last component supplied to make up for missing components.
  // 不足しているコンポーネントを補うために、最後に提供されたコンポーネントのオーバーフローを再計算します。
  ipAdress[4 + ipAdress[0]] *= Math.pow(256, 4 - ipAdress[0]);
  if (ipAdress[1] >= ipAdress[5] || ipAdress[2] >= ipAdress[6] || ipAdress[3] >= ipAdress[7] || ipAdress[4] >= ipAdress[8]) {
    return false;
  }
  return ipAdress[1] * (ipAdress[0] === 1 || 16777216) + ipAdress[2] * (ipAdress[0] <= 2 || 65536) + ipAdress[3] * (ipAdress[0] <= 3 || 256) + ipAdress[4] * 1;
}


var longToIp = function(ipAdress) {
  if (!isFinite(ipAdress))
    return false;

  return [ipAdress >>> 24, ipAdress >>> 16 & 0xFF, ipAdress >>> 8 & 0xFF, ipAdress & 0xFF].join('.');
}

var nwAdress = function(ipAdress, subnetMask) {
  return longToIp(ipToLong(ipAdress) & ipToLong(subnetMask));
}

var cidrToSubnetmask = function(cidr) {
  var mask = [], i, n;
  for(i=0; i<4; i++) {
    n = Math.min(cidr, 8);
    mask.push(256 - Math.pow(2, 8-n));
    cidr -= n;
  }
  return mask.join('.');
}

var subnetmaskToCidr = function(subnetmask) {

  var subnetmaskNodes = subnetmask.match(/(\d+)/g);
  var cidr = 0;
  for(var i in subnetmaskNodes){
    cidr += (((subnetmaskNodes[i] >>> 0).toString(2)).match(/1/g) || []).length;
  }
  return cidr;
}