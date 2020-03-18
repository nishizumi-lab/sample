import 'package:flutter/material.dart';

class PaddingPage extends StatefulWidget {
  PaddingPage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _PaddingPageState createState() => _PaddingPageState();
}

class _PaddingPageState extends State<PaddingPage> {

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        // アプリケーションバーの上の空白
        Container(color: Colors.white, width: double.infinity, height: 100,),
        Expanded(
          child: Scaffold(
            appBar: new AppBar(
              title: new Text('Page Title'),
            ),
            body: new Center(
              child: new Text('Hello World'),
            ),
            // 下部ナビゲーションバーでスクロール
            bottomNavigationBar: BottomNavigationBar(
              currentIndex: 0,
              items: [
                new BottomNavigationBarItem(
                    icon: new Icon(Icons.home),
                    title: Text("Test")
                ),
                new BottomNavigationBarItem(
                    icon: new Icon(Icons.settings),
                    title: Text("Test")
                ),
              ],
            ),
          ),
        ),
        // ナビゲーションバーの下の空白
        Container(color: Colors.white, width: double.infinity, height: 100,),
      ],
    );
  }
}