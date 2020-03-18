import 'package:flutter/material.dart';

class LoadJsonDetailPage extends StatefulWidget {
  var jsonData = {}; // ページ1の入力値保持用

  LoadJsonDetailPage(var jsonData) {
    this.jsonData = jsonData;
  }

  @override
  _LoadJsonDetailPageState createState() => _LoadJsonDetailPageState(jsonData);
}

class _LoadJsonDetailPageState extends State<LoadJsonDetailPage> {
  var jsonData = {}; // ページ1の入力値保持用
  _LoadJsonDetailPageState(var jsonData) {
    this.jsonData = jsonData;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: new AppBar(
        title: new Text('Page Title'),
      ),

      body: ListView(
        children: <Widget>[
          ListTile(
            leading: Icon(Icons.map),
            title: Text(jsonData["id"]),
          ),
          ListTile(
            leading: Icon(Icons.photo_album),
            title: Text(jsonData["name"]),
          ),
          ListTile(
            leading: Icon(Icons.phone),
            title: Text(jsonData["point"].toString()),
          ),
        ],
      ),
    );
  }
}
