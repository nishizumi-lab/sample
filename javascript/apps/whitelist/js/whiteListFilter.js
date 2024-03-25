function whiteListFilter(){
    const startTime = Date.now();

    var inputData = document.getElementById('inputArea').value;
    var whiteListData = document.getElementById('whiteListArea').value;
    var inputArray = inputData.split("\n");
    var whiteListArray = whiteListData.split("\n");
    //var statusArea = doccument.getElementById("aaa");

    var whiteListLength = whiteListArray.length;

    var j = 0;

    for(const whiteStr of whiteListArray){
        var i = 0;
        //statusArea.innerHTML = '■進捗:' + String(j) + '/' + String(whiteListLength) + '件完了';
        for(const inputStr of inputArray){
            if(inputStr.indexOf(whiteStr) > -1){
                inputArray[i] = "DELETE";
            }
            i = i + 1;
        }
        j = j + 1;        
    }

    //var outputArray = Array.from(new Set(inputArray));
    var outputArray = inputArray;
    var output = document.getElementById('outputArea');
    output.innerHTML = "";

    var i = 0;
    
    while(i < inputArray.length){
        output.innerHTML += outputArray[i] + "\n";
        i = i + 1;
    }

    const endTime = Date.now();
    //statusInfo.innerHTML = statusInfo.innerHTML + '■処理時間:' + String(endTime - startTime) + "[msec]";
}
