import 'package:flutter/material.dart';
import 'package:navigator/screens/home_page.dart';
import 'package:navigator/screens/setting_page.dart';
import 'package:navigator/screens/scroll_page.dart';
import 'package:navigator/screens/padding_page.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Test App',
      theme: new ThemeData.dark(),
      //home: HomePage(title: 'Home Page'),
      home: PaddingPage(title: 'Padding Page'),
      //home: ScrollPage(title: 'Home Page'),
      // ルートを事前に定義
      // ルーティング名称に対して、表示されるページを作成しウィジェットを設定
      routes: <String, WidgetBuilder> {
        //'/home': (BuildContext context) => new HomePage(),
        '/padding': (BuildContext context) => new PaddingPage(),
        '/setting': (BuildContext context) => new SettingPage()
      },
    );
  }
}