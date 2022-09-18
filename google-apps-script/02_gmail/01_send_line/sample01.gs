// LINEトークン
var LINE_NOTIFY_TOKEN = "XXXXXXXXXXX";

// LINEに通知する条件(訓練という単語が含まれている未読メールを検索)
var query = "訓練 is:unread";
 
// Gmailを取得(条件に該当するメールがあればLINEに通知)
function getGmail(){
 
  // 指定した検索条件でGmailからスレッド取得
  var threads = GmailApp.search(query, 0, 10);
  
  // 取得したスレッド二次元配列に格納
  var messages = GmailApp.getMessagesForThreads(threads);
  
 
  for(var i in messages){
    for(var j in messages[i]){

        // 送信元を取得
        var fromaddress = messages[i][j].getFrom() + "\n"; 

        // タイムスタンプを取得
        var date = Utilities.formatDate(messages[i][j].getDate(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm:ss')+"\n"; 
        
        // 件名を取得
        var subject = messages[i][j].getSubject() + "\n"; 

        // 本文の冒頭500文字を取得
        var body= messages[i][j].getPlainBody().slice(0, 500);

        
        // LINEにメッセージを送信
        sendLine(fromaddress + date + subject + body);
 
        // 取得したメッセージを既読にする
        messages[i][j].markRead();
    }
  }
}

// LINEに通知
function sendLine(msg) {
  var response = UrlFetchApp.fetch("https://notify-api.line.me/api/notify", {
    "method": "post",
    "headers": {
      "Authorization": "Bearer " + LINE_NOTIFY_TOKEN
    },
    "payload": {
      "message": msg
    }
  });
}