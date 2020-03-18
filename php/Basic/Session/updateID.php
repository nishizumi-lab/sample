<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Test</title>

<?php

// セッション開始
session_start();
// 古いID取得
$id1 = session_id();
// ID更新
session_regenerate_id(True);
// 新しいID取得
$id2 = session_id();
// セッションIDの表示
print "旧ID：$id1<br>"; // 旧ID：80btpbli6gakr19bogbqfhol23
print "新ID：$id2"; // 新ID：brf85v2ju91qe88mtgbn314qg5 

?>
</head>
  
<body>
</body>
</html>
