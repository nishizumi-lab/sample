import 'package:flutter/material.dart';
import 'package:basic/utils/todo.dart';

class Todo1NewPage extends StatefulWidget {
  final Todo item;

  Todo1NewPage({ this.item });

  @override
  _Todo1NewPageState createState() => _Todo1NewPageState();
}

class _Todo1NewPageState extends State<Todo1NewPage> {
  TextEditingController titleController;

  @override
  void initState() {
    super.initState();
    titleController = new TextEditingController(
      text: widget.item != null ? widget.item.title : null
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.item != null ? 'Edit todo' : 'New todo',
          key: Key('new-item-title'),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              controller: titleController,
              autofocus: true,
              decoration: InputDecoration(labelText: 'Title'),
            ),
            TextField(
              //controller: dateController,
              autofocus: true,
              decoration: InputDecoration(labelText: 'Date'),
            ),
            SizedBox(height: 14.0,),
            RaisedButton(
              color: Theme.of(context).primaryColor,
              child: Text(
                'Save',
                style: TextStyle(
                  color: Theme.of(context).primaryTextTheme.title.color
                ),
              ),
              elevation: 3.0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(10.0),
                  topRight: Radius.circular(10.0)
                )
              ),
              onPressed: () => submit(),
            )
          ],
        ),
      ),
    );
  }

  void submit(){
    Navigator.of(context).pop(titleController.text);
  }
}