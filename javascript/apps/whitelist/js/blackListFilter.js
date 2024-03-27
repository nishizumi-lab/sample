function blackListFilter(){
    const startTime = Date.now();

    var outputData = document.getElementById('outputArea').value;
    var outputArray = outputData.split("\n").filter(Boolean);

    var blackListData = document.getElementById('blacklistArea').value;
    var blackListArray = blackListData.split("\n").filter(Boolean);
    let blacklistedArray = [];
    let unblacklistedArray = [];
    var blacklistedFlag = 0;
    var statusArea2 = document.getElementById("statusArea2");
    var j = 0;

    for(const outputStr of outputArray){
        blacklistedFlag = 0;
        statusArea2.innerHTML = '2️⃣ブラックリストで抽出:' + String(j+1) + '/' + String(outputArray.length) + '件完了';
        for(const blackStr of blackListArray){
            if(outputStr.indexOf(blackStr) > -1){
                blacklistedArray.push(outputStr);
                blacklistedFlag = 1;
            }
        }
        if(blacklistedFlag == 0){
            //console.log(outputStr);
            unblacklistedArray.push(outputStr);
        }      
        j++;
    }
    //console.log(unblacklistedArray);


    var blacklistedArea = document.getElementById('blacklistedArea');
    blacklistedArea.innerHTML = "";

    var unblacklistedArea = document.getElementById('unblacklistedArea');
    unblacklistedArea.innerHTML = "";

    var i = 0;
    var j = 0;

    while(i < blacklistedArray.length){
        blacklistedArea.innerHTML += blacklistedArray[i] + "\n";
        i = i + 1;
    }

    while(j < unblacklistedArray.length){
        unblacklistedArea.innerHTML += unblacklistedArray[j] + "\n";
        j = j + 1;
    }

    const endTime = Date.now();
    statusArea2.innerHTML += ', 処理時間:' + String(endTime - startTime) + "[msec]\n";
}