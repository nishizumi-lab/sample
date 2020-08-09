import 'package:flutter/material.dart';
import 'dart:math';

class Textform1Page extends StatefulWidget {
  Textform1Page({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _Textform1PageState createState() => _Textform1PageState();
}

class _Textform1PageState extends State<Textform1Page> {
  var _date = DateTime.now();
  // テキストフィールドの管理用コントローラを作成
  final _voltageController = TextEditingController();
  final _currentController = TextEditingController();
  final _resistorController = TextEditingController();
  // データ格納用リスト
  List<Map<String, dynamic>> items = [
    {"id": 1, "title": "title1"},
    {"id": 2, "title": "title2"},
  ];

  //　上記リストのカウント変数（ID用）
  int _counter = 2;
  final String text = "Flutter";

  List<String> _currentUnits = ["kA", "A", "mA", "μA"];
  String _selectedCurrentUnit = "A";
  List<String> _voltageUnits = ["kV", "V", "mV", "μV"];
  String _selectedVoltageUnit = "A";
  List<String> _resistorUnits = ["MΩ", "kΩ", "Ω", "mΩ", "μΩ"];
  String _selectedResistorUnit = "Ω";

  //　テキストフィールドに入力されたアイテムをリストに追加（投稿ボタンが押されたときに呼び出す関数）
  void _addItem(String inputtext) {
    setState(() {
      _counter++;
      items.add({"id": _counter, "title": inputtext});
    });
  }

  @override
  // widgetの破棄時にコントローラも破棄する
  void dispose() {
    _voltageController.dispose();
    _currentController.dispose();
    _resistorController.dispose();
    super.dispose();
  }
  /*
  @override
  // widgetの破棄時にコントローラも破棄する
  void dispose() {
    myController.dispose();
    super.dispose();
  }*/

  @override
  Widget build(BuildContext context) {
    return Column(children: <Widget>[
      Expanded(
        child: Scaffold(
          appBar: AppBar(
            title: Text("直流電流計算機", style: TextStyle(color: Colors.white)),
            /*
            actions: <Widget>[
              IconButton(
                icon: Icon(Icons.event_note),
                onPressed: () => setState(() {
                  Navigator.of(context).pushNamed("/shuki");
                }),
              ),
            ],*/
          ),
          // ListviewでJSONデータを表示
          body: Container(
            child: Column(
              // mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  // テキストフィールド
                  Padding(
                    padding: const EdgeInsets.all(5.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween, // これで両端に寄せる
                      children: <Widget>[
                        Text("電圧：",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                        new Container(
                            width: 170.0,
                            child: new TextField(
                              controller: _voltageController,
                              keyboardType: TextInputType.number, // キーボードは数値のみ
                                style: new TextStyle(
                                    fontSize: 18.0,
                                    height: 1.0,
                                    color: Colors.black
                                ),
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              onChanged: (value) {
                                setState(() {
                                  _currentController.text =  (int.parse(_voltageController.text) /  int.parse(_resistorController.text)).toString();
                                });
                              },
                            )
                        ),
                        DropdownButton<String>(
                          value: _selectedCurrentUnit,
                          onChanged: (String newValue) {
                            setState(() {
                              _selectedCurrentUnit = newValue;
                            });
                          },
                          selectedItemBuilder: (context) {
                            return _currentUnits.map((String item) {
                              return Text(
                                item,
                                style: TextStyle(color: Colors.pink),
                              );
                            }).toList();
                          },
                          items: _currentUnits.map((String item) {
                            return DropdownMenuItem(
                              value: item,
                              child: Text(
                                item,
                                style: item == _selectedCurrentUnit
                                    ? TextStyle(fontWeight: FontWeight.bold)
                                    : TextStyle(fontWeight: FontWeight.normal),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                  // リストビュー
                  Padding(
                    padding: const EdgeInsets.all(5.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween, // これで両端に寄せる
                      children: <Widget>[
                        Text("電流：",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                        new Container(
                            width: 170.0,
                            child: new TextField(
                              controller: _currentController,
                              keyboardType: TextInputType.number, // キーボードは数値のみ
                              style: new TextStyle(
                                  fontSize: 18.0,
                                  height: 1.0,
                                  color: Colors.black
                              ),
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              onChanged: (value) {
                                setState(() {
                                  //_text = value;
                                });
                              },
                            )
                        ),
                        DropdownButton<String>(
                          value: _selectedCurrentUnit,
                          onChanged: (String newValue) {
                            setState(() {
                              _selectedCurrentUnit = newValue;
                            });
                          },
                          selectedItemBuilder: (context) {
                            return _currentUnits.map((String item) {
                              return Text(
                                item,
                                style: TextStyle(color: Colors.pink),
                              );
                            }).toList();
                          },
                          items: _currentUnits.map((String item) {
                            return DropdownMenuItem(
                              value: item,
                              child: Text(
                                item,
                                style: item == _selectedCurrentUnit
                                    ? TextStyle(fontWeight: FontWeight.bold)
                                    : TextStyle(fontWeight: FontWeight.normal),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(5.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween, // これで両端に寄せる
                      children: <Widget>[
                        Text("抵抗：",
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                        new Container(
                            width: 170.0,
                            child: new TextField(
                              controller: _resistorController,
                              keyboardType: TextInputType.number, // キーボードは数値のみ
                              style: new TextStyle(
                                  fontSize: 18.0,
                                  height: 1.0,
                                  color: Colors.black
                              ),
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              onChanged: (value) {
                                setState(() {
                                  //_text = value;
                                });
                              },
                            )
                        ),
                        DropdownButton<String>(
                          value: _selectedCurrentUnit,
                          onChanged: (String newValue) {
                            setState(() {
                              _selectedCurrentUnit = newValue;
                            });
                          },
                          selectedItemBuilder: (context) {
                            return _currentUnits.map((String item) {
                              return Text(
                                item,
                                style: TextStyle(color: Colors.pink),
                              );
                            }).toList();
                          },
                          items: _currentUnits.map((String item) {
                            return DropdownMenuItem(
                              value: item,
                              child: Text(
                                item,
                                style: item == _selectedCurrentUnit
                                    ? TextStyle(fontWeight: FontWeight.bold)
                                    : TextStyle(fontWeight: FontWeight.normal),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ]),
          ),
        ),
      ),
      // ナビゲーションバーの下の空白
    ]);
  }
  void onPressed() async {
    // showDatePicker() の引数で locale を指定
    var selectedDate = await showDatePicker(
      context: context,
      locale: const Locale("ja"),
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime(2050),
      builder: (BuildContext context, Widget widget) {
        return widget;
      },
    );

    if (selectedDate != null) {
      setState(() {
        _date = selectedDate;
        //_chuinMap = calender.yearToChuin(_date);
      });
    }
  }
}