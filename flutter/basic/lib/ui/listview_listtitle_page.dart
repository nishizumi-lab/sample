import 'package:flutter/material.dart';

class ListviewListtitlePage extends StatefulWidget {
  ListviewListtitlePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _ListviewListtitlePageState createState() => _ListviewListtitlePageState();
}

class _ListviewListtitlePageState extends State<ListviewListtitlePage> {
  var listItem = ["Savar", "Archer", "Lancer", "Rider", "Caster", "Assassin", "Berserker", "Ruler", "Avenger", "Alterego", "Mooncancer"];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('List Test'),),
      body: ListView.builder(
        itemBuilder: (BuildContext context, int index) {
          return Container(
              decoration: BoxDecoration(
                border: Border(
                  bottom: BorderSide(color: Colors.black38),
                ),
              ),
              child: ListTile(
                leading: const Icon(Icons.done),
                title: Text(listItem[index]),
                subtitle: Text('$index'),
                onTap: () { /* react to the tile being tapped */ },
              ));},
        itemCount: listItem.length,
      ),
    );
  }
}