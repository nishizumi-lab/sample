//文字列の類似度チェック
levenshteinDistance = function(str1, str2) {
    let r, c, cost,
        d = [];
   
    for (r=0; r<=str1.length; r++) {
      d[r] = [r];
    }
    for (c=0; c<=str2.length; c++) {
      d[0][c] = c;
    }
    for (r=1; r<=str1.length; r++) {
      for (c=1; c<=str2.length; c++) {
        cost = str1.charCodeAt(r-1) == str2.charCodeAt(c-1) ? 0: 1;
        d[r][c] = Math.min(d[r-1][c]+1, d[r][c-1]+1, d[r-1][c-1]+cost);
      }
    }
    return d[str1.length][str2.length];
}

function levenFilter(){
    const startTime = Date.now();

    var unblacklistedData = document.getElementById('unblacklistedArea').value;
    var unblacklistedArray = unblacklistedData.split("\n").filter(Boolean);

    var blackListData = document.getElementById('blacklistArea').value;
    var blackListArray = blackListData.split("\n").filter(Boolean);
    var statusArea3 = document.getElementById("statusArea3");

    let dangerArray = [];
    let safetyArray = [];
    var dangerFlag = 0;

    var j = 0;

    for(const unblacklistedStr of unblacklistedArray){
        dangerFlag = 0;
        statusArea3.innerHTML = '3️⃣ブラックリストとの類似度計算:' + String(j+1) + '/' + String(unblacklistedArray.length) + '件完了';
        for(const blackStr of blackListArray){
            var score = levenshteinDistance(blackStr, unblacklistedStr);
            if(score <= 4){
                dangerFlag = 0;
            }
            else{
                dangerFlag = 1;                
            }
        }
        if(dangerFlag == 0){
            dangerArray.push(unblacklistedStr);
        }
        else{
            safetyArray.push(unblacklistedStr);           
        }      
        j++;
    }
    //console.log(unblacklistedArray);


    var safetyArea = document.getElementById('safetyArea');
    safetyArea.innerHTML = "";

    var dangerArea = document.getElementById('dangerArea');
    dangerArea.innerHTML = "";

    var i = 0;
    var j = 0;

    while(i < safetyArray.length){
        safetyArea.innerHTML += safetyArray[i] + "\n";
        i = i + 1;
    }

    while(j < dangerArray.length){
        dangerArea.innerHTML += dangerArray[j] + "\n";
        j = j + 1;
    }

    const endTime = Date.now();
    statusArea3.innerHTML += ', 処理時間:' + String(endTime - startTime) + "[msec]\n";
}
