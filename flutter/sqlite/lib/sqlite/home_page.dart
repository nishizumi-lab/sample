import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  HomePage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentIndex = 0; // currentIndexにデフォルト値を与えないとコンパイルエラーにな
  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar: new AppBar(
        title: new Text('HomePage'),
      ),
      body: new Container(
        padding: new EdgeInsets.all(32.0),
        child: new Center(
          child: new Column(
            children: <Widget>[
              Text('Home'),
              // ①ボタンでページ遷移
              // 遷移するにはNavigator.of(context).pushNamedに対して遷移先の名称を渡すことで、対象のウィジェットを呼び出し
              // 呼び出されたウィジェットはHomePageの上にSettingPageになりナビゲーションヘッダーに戻るボタンが表示される
              RaisedButton(onPressed: () => Navigator.of(context).pushNamed("/setting"), child: new Text('設定ページ'),)
            ],
          ),
        ),
      ),

      // ② 下部ナビゲーションバーでページ遷移
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        items: [
          new BottomNavigationBarItem(
              icon: new Icon(Icons.home),
              title: Text("ホーム")
          ),
          new BottomNavigationBarItem(
              icon: new Icon(Icons.settings),
              title: Text("設定")
          ),
        ],
        // ナビゲーションバーのいずれかのボタンがタップされたら
        onTap: (int index) {
          print(index); // デバッグ用に出力（タップされたボタンによって数値がかわる）
          if(index == 0){
            Navigator.of(context).pushNamed("/home");
          }
          else if(index == 1){
            Navigator.of(context).pushNamed("/setting");
          }
        },
      ),
    );
  }
}