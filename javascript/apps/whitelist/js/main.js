function main(){
    var inputData = document.getElementById('inputArea').value;
    var whiteListData = document.getElementById('whiteListArea').value;
    var inputArray = inputData.split("\n");
    var whiteListArray = whiteListData.split("\n");

    console.log("Input Data");
    console.log(inputArray);
    
    
    for(const whiteStr of whiteListArray){
        var i = 0;
        for(const inputStr of inputArray){
            if(inputStr.indexOf(whiteStr) > -1){
                inputArray[i] = "DELETE";
            }
            i = i + 1;

        }
    }
    
    console.log("Output Data");
    console.log(inputArray);

    // 重複要素を削除
    var outputArray = Array.from(new Set(inputArray));
    
    console.log("outputArray");
    console.log(outputArray);

    var output = document.getElementById('outputArea');
    output.innerHTML = "";
    
    var i = 0;
    
    while(i < inputArray.length){
        output.innerHTML += inputArray[i] + "\n";
        i = i + 1;
    }
}
