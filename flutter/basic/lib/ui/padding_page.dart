import 'package:flutter/material.dart';
import 'package:basic/main.dart';

class PaddingPage extends StatefulWidget {
  @override
  PaddingPageState createState() => PaddingPageState();
}

class PaddingPageState extends State<PaddingPage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: new AppBar(
        title: new Text('Page Title'),
      ),
      body: new Center(
        child: new Text('Hello World'),
      ),
    );
  }
}