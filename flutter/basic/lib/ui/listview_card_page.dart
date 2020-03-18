import 'package:flutter/material.dart';

class ListviewCardPage extends StatefulWidget {
  ListviewCardPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _ListviewCardPageState createState() => _ListviewCardPageState();
}

class _ListviewCardPageState extends State<ListviewCardPage> {
  var listItem = ["Savar", "Archer", "Lancer", "Rider", "Caster", "Assassin", "Berserker", "Ruler", "Avenger", "Alterego", "Mooncancer"];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Test'),),
      body: ListView.builder(
        itemBuilder: (BuildContext context, int index) {
          return Card(
            child: Padding(
              child: Text('$index ：' + listItem[index], style: TextStyle(fontSize: 22.0),),
              padding: EdgeInsets.all(20.0),),
          );},
        itemCount: listItem.length,),
    );
  }
}