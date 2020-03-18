import 'package:flutter/material.dart';
import 'package:basic/utils/todo.dart';
import 'package:basic/ui/todo1_new_page.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:basic/main.dart';

class Todo1Page extends StatefulWidget {
  @override
  Todo1PageState createState() => Todo1PageState();
}

class Todo1PageState extends State<Todo1Page> with SingleTickerProviderStateMixin{
  List<Todo> items = new List<Todo>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(
            'FlutterTodo',
            key: Key('main-app-title'),
          ),
          centerTitle: true,
        ),
        floatingActionButton: FloatingActionButton(
          child: Icon(Icons.add),
          onPressed: () =>goToNewItemView(),
        ),
        body: renderBody()
    );
  }

  Widget renderBody(){
    if(items.length > 0){
      return buildListView();
    }else{
      return emptyList();
    }
  }

  Widget emptyList(){
    return Center(
        child:  Text('No items')
    );
  }


  Widget buildListView() {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (BuildContext context,int index){
        return buildItem(items[index], index);
      },
    );
  }

  Widget buildItem(Todo item, index){
    return Dismissible(
      key: Key('${item.hashCode}'),
      background: Container(color: Colors.red[700]),
      onDismissed: (direction) => _removeItemFromList(item),
      direction: DismissDirection.startToEnd,
      child: buildListTile(item, index),
    );
  }

  Widget buildListTile(item, index){
    return ListTile(
      onTap: () => changeItemCompleteness(item),
      onLongPress: () => goToEditItemView(item),
      title: Text(
        "$index:" + item.title,
        key: Key('item-$index'),
        style: TextStyle(
            decoration: item.completed ? TextDecoration.lineThrough : null
        ),
      ),
      subtitle: Text(item.date),
      trailing: Icon(item.completed
          ? Icons.check_box
          : Icons.check_box_outline_blank,
        key: Key('completed-icon-$index'),
      ),
    );
  }

  void changeItemCompleteness(Todo item){
    setState(() {
      item.completed = !item.completed;
    });
  }

  void goToNewItemView(){
    Navigator.of(context).push(MaterialPageRoute(builder: (context){
      return Todo1NewPage();
    })).then((title){
      if(title != null) {
        addItem(Todo(title: title));
      }
    });
    Navigator.of(context).push(MaterialPageRoute(builder: (context){
      return Todo1NewPage();
    })).then((date){
      if(date != null) {
        addItem(Todo(date: date));
      }
    });
  }

  void addItem(Todo item){
    items.insert(0, item);
  }

  void goToEditItemView(item){
    Navigator.of(context).push(MaterialPageRoute(builder: (context){
      return Todo1NewPage(item: item);
    })).then((title){
      if(title != null) {
        editItem(item, title);
      }
    });
    Navigator.of(context).push(MaterialPageRoute(builder: (context){
      return Todo1NewPage(item: item);
    })).then((date){
      if(date != null) {
        editItem(item, date);
      }
    });
  }

  void editItem(Todo item ,String title){
    item.title = title;
  }

  void editDate(Todo item ,String date){
    item.date = date;
  }

  void _removeItemFromList(item) {
    deleteItem(item);
  }

  void deleteItem(item){
    items.remove(item);
  }
}