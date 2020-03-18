import 'package:flutter/material.dart';
//import 'package:basic/ui/home_page.dart';
//import 'package:basic/ui/listview_card_page.dart';
//import 'package:basic/ui/listview_listtitle_page.dart';
//import 'package:basic/ui/todo1_page.dart';
//import 'package:basic/ui/json_table1_page.dart';
//import 'package:basic/ui/todo1_page.dart';
//import 'package:basic/ui/padding_page.dart';
//import 'package:basic/ui/load_json_page.dart';
import 'package:basic/ui/load_json2_page.dart';
import 'package:basic/ui/load_json_detail_page.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Test App',
      theme: new ThemeData.dark(),
      // home: HomePage(title: 'Home Page'),
      // home:ListviewCardPage(title: 'Test'),
      // home:ListviewListtitlePage(title: 'Test'),
      // home:Todo1Page(title: 'Test'),
      // home:JsonTable1Page(),
      //home:PaddingPage(),
      //home:PaddingPage(),
      //home:LoadJsonPage(),
      home:LoadJson2Page(),
      // ルートを事前に定義
      // ルーティング名称に対して、表示されるページを作成しウィジェットを設定
      routes: <String, WidgetBuilder> {
        //'/home': (BuildContext context) => new HomePage(),
        '/load_json_detail': (BuildContext context) => new LoadJsonDetailPage({})
      },
    );
  }
}