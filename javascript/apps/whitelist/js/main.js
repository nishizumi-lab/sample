function main(){
    // 2次元配列の宣言・初期化
    var inputData = document.getElementById('inputArea').value;
    var whiteListData = document.getElementById('whiteListArea').value;
    var inputArray = inputData.split(~inputData.indexOf("\r\n")?"\r\n":"\n");
    var whiteListArray = whiteListData.split(~whiteListData.indexOf("\r\n")?"\r\n":"\n");
    console.log(inputArray);
    for(const whiteStr of whiteListArray){
        const indexOfPigeon = inputArray.findIndex(animal => animal.includes(whiteStr))
        inputArray.splice(indexOfPigeon, 1);
    }
    console.log(inputArray);
    var output = document.getElementById('outputArea');
    var i = 0;
    while(i < inputArray.length){
        output.innerHTML += inputArray[i] + "\n";
        i = i + 1;
    }
}
