import 'package:flutter/material.dart';
import 'dart:async';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:flutter/material.dart';
//import 'package:stat/stat.dart';

class TestPage extends StatefulWidget {
  TestPage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _TestPageState createState() => _TestPageState();
}

class _TestPageState extends State<TestPage> {
  int _currentIndex = 0; // currentIndexにデフォルト値を与えないとコンパイルエラーにな
  //var stat = new Stat();
  //var list = [1, 2, 3, 4, 5];

  // 合計の計算
  //num sum_value = stat.sum(list);
  //print(sum_value); // 15
  @override
  Widget build(BuildContext context) {
    //test();
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

void test() async {
  final database = openDatabase(
    join(await getDatabasesPath(), 'memo_database.db'),
    onCreate: (db, version) {
      return db.execute(
        "CREATE TABLE memo(id INTEGER PRIMARY KEY, text TEXT, priority INTEGER)",
      );
    },
    version: 1,
  );

  Future<void> insertMemo(Memo memo) async {
    final Database db = await database;
    await db.insert(
      'memo',
      memo.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<Memo>> getMemos() async {
    final Database db = await database;
    final List<Map<String, dynamic>> maps = await db.query('memo');
    return List.generate(maps.length, (i) {
      return Memo(
        id: maps[i]['id'],
        text: maps[i]['text'],
        priority: maps[i]['priority'],
      );
    });
  }

  Future<void> updateMemo(Memo memo) async {
    // Get a reference to the database.
    final db = await database;
    await db.update(
      'memo',
      memo.toMap(),
      where: "id = ?",
      whereArgs: [memo.id],
      conflictAlgorithm: ConflictAlgorithm.fail,
    );
  }

  Future<void> deleteMemo(int id) async {
    final db = await database;
    await db.delete(
      'memo',
      where: "id = ?",
      whereArgs: [id],
    );
  }

  var memo = Memo(
    id: 0,
    text: 'Flutterで遊ぶ',
    priority: 1,
  );

  await insertMemo(memo);

  print(await getMemos());

  memo = Memo(
    id: memo.id,
    text: memo.text,
    priority: memo.priority + 1,
  );
  await updateMemo(memo);

  // Print Fido's updated information.
  print(await getMemos());

  // Delete Fido from the database.
  await deleteMemo(memo.id);

  // Print the list of dogs (empty).
  print(await getMemos());
}

class Memo {
  final int id;
  final String text;
  final int priority;

  Memo({this.id, this.text, this.priority});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'text': text,
      'priority': priority,
    };
  }
  @override
  String toString() {
    return 'Memo{id: $id, tet: $text, priority: $priority}';
  }
}