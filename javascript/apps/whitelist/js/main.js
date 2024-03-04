function main(){
    var inputData = document.getElementById('inputArea').value;
    var whiteListData = document.getElementById('whiteListArea').value;
    var inputArray = inputData.split(~inputData.indexOf("\r\n")?"\r\n":"\n");
    var whiteListArray = whiteListData.split(~whiteListData.indexOf("\r\n")?"\r\n":"\n");

    console.log("Input Data");
    console.log(inputArray);
    
    
    for(const whiteStr of whiteListArray){
        const indexOfPigeon = inputArray.findIndex(animal => animal.includes(whiteStr))
        inputArray.splice(indexOfPigeon, 1);
    }
    
    console.log("Output Data");
    console.log(inputArray);

    // 重複要素を削除
    var outputArray = new Set(inputArray);
    
    var output = document.getElementById('outputArea');
    output.innerHTML = "";
    var i = 0;
    
    while(i < inputArray.length){
        output.innerHTML += inputArray[i] + "\n";
        i = i + 1;
    }
}
