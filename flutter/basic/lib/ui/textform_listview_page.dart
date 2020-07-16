import 'package:flutter/material.dart';

class TextformListviewPage extends StatefulWidget {
  TextformListviewPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _TextformListviewPageState createState() => _TextformListviewPageState();
}

class _TextformListviewPageState extends State<TextformListviewPage> {

  // テキストフィールドの管理用コントローラを作成
  final myController = TextEditingController();

  // データ格納用リスト
  List<Map<String, dynamic>> items = [
    { "id" : 1,  "title" : "title1" },
    { "id" : 2,  "title" : "title2" },
  ];

  //　上記リストのカウント変数（ID用）
  int _counter = 2;

  //　テキストフィールドに入力されたアイテムをリストに追加（投稿ボタンが押されたときに呼び出す関数）
  void _addItem(String inputtext) {
    setState(() {
      _counter++;
      items.add({ "id": _counter, "title": inputtext});
    });
  }

  @override
  // widgetの破棄時にコントローラも破棄する
  void dispose() {
    myController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Test title'),
      ),
      body: Container (
         child: Column(
          // mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // テキストフィールド
            Padding(
              padding: const EdgeInsets.all(17.0),
              child: TextField(
                controller: myController,
              ),
            ),
            // リストビュー
            Expanded(
              child:ListView.builder(
              scrollDirection: Axis.vertical,
              shrinkWrap: true,
              itemCount: items.length,
              itemBuilder: (BuildContext context, int index) {
              final item = items[index];
            
              return new Card(
                child: ListTile(
                  leading: Icon(Icons.people),
                  title: Text(item["id"].toString() + " : " + item["title"]),
                ),
              );
            }),
            ),
          ]),
        ),
        // 投稿ボタン
        floatingActionButton: FloatingActionButton(
        // onPressedでボタンが押されたらテキストフィールドの内容を取得して、アイテムに追加
        onPressed: () {
          _addItem(myController.text);
          // テキストフィールドの内容をクリア
          myController.clear();
        },
        child: Icon(Icons.add),
      ),
    );
  }
}