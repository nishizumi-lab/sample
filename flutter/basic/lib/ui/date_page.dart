import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:intl/intl.dart';

class DatePage extends StatefulWidget {
  DatePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _DatePageState createState() => _DatePageState();
}

class _DatePageState extends State<DatePage> {

  var _date = DateTime.now();

  @override
  Widget build(BuildContext context) {
    var format = new DateFormat.yMMMd('ja');

    return Scaffold(
      appBar: AppBar(title: Text('日付設定')),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
                padding: EdgeInsets.only(left:20.0, right:20, top:5),
                child:            Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween, // これで両端に寄せる
                  children: <Widget>[
                    Text(format.format(_date),

                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                        color: Theme.of(context).primaryColor,
                      ),
                    ),
                    RaisedButton(
                      child: Text('日付を設定',
                        style: TextStyle(
                            fontSize: 16.0
                        ),),
                      onPressed: onPressed,
                      color: Colors.white70,
                      highlightColor: Theme.of(context).primaryColor,
                    ),
                  ],
                ),
            ),
          ],
        ),
      ),
    );
  }

  void onPressed() async {
    // showDatePicker() の引数で locale を指定
    var selectedDate = await showDatePicker(
      context: context,
      locale: const Locale("ja"),
      initialDate: DateTime.now(),
      firstDate: DateTime(2018),
      lastDate: DateTime(2030),
      builder: (BuildContext context, Widget widget) {
        return widget;
      },
    );

    if (selectedDate != null) {
      setState(() {
        _date = selectedDate;
      });
    }
  }
}