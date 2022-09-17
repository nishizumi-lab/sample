// LINEトークン
var LINE_NOTIFY_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXX";

// LINEに通知する条件(件名、メールアドレス、内容)
var query = "subject:(テスト) from:xxxx@gmail.com";
 
 
// Gmailをチェック(条件に該当するメールがあればLINEに通知)
function checkGmail(){
 
  // 指定した条件でGmailのスレッドを検索 
  var threads = GmailApp.search(query, 0, 10);
  
  // 検索してヒットしたメールの内容を取得し二次元配列に格納
  var messages = GmailApp.getMessagesForThreads(threads);
  
 
  for(var i in messages){
    for(var j in messages[i]){
      //スターがないメッセージのみ処理   
      if(!myMessages[i][j].isStarred()){ 
   var date　=　messages[i][j].getDate();
        var msg = Utilities.formatDate(messages[i][j].getDate(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm:ss')+"\n"; //タイムスタンプ
        msg += messages[i][j].getSubject() + "\n"; // 件名
        msg += messages[i][j].getPlainBody().slice(0, 100); // 冒頭100文字のみ抽出
        
        // LINEにメッセージを送信
        sendLine(msg);
 
        //処理済みのメッセージをスターをつける
        messages[i][j].star(); 
    }
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