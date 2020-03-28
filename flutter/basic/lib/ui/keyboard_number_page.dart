import 'package:flutter/material.dart';
import 'package:basic/utils/keyboard_number_parser.dart';

const appName = 'シンプル電卓';

class KeyboardNumberPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      body: new Column(
        children: [
          new Display(),
          new Keyboard(),
        ],
      ),
    );
  }
}

var _displayState = new DisplayState();

class Display extends StatefulWidget {
  @override
  State createState() {
    return _displayState;
  }
}

class DisplayState extends State {
  var _expression = '';
  var _result = '';

  @override
  Widget build(BuildContext context) {
    var views = [
      new Expanded(
          flex: 1,
          child: new Row(
            children: [
              new Expanded(
                  child: new Text(
                    _expression,
                    textAlign: TextAlign.right,
                    style: new TextStyle(
                      fontSize: 40.0,
                      color: Colors.white,
                    ),
                  ))
            ],
          )),
    ];

    if (_result.isNotEmpty) {
      views.add(new Expanded(
          flex: 1,
          child: new Row(
            children: [
              new Expanded(
                  child: new Text(
                    _result,
                    textAlign: TextAlign.right,
                    style: new TextStyle(
                      fontSize: 40.0,
                      color: Colors.white,
                    ),
                  ))
            ],
          )),
      );
    }

    return new Expanded(
        flex: 2,
        child: new Container(
          color: Theme
              .of(context)
              .primaryColor,
          padding: const EdgeInsets.all(16.0),
          child: new Column(
            children: views,
          ),
        ));
  }
}

void _addKey(String key) {
  var _expr = _displayState._expression;
  var _result = '';
  if (_displayState._result.isNotEmpty) {
    _expr = '';
    _result = '';
  }

  if (operators.contains(key)) {
    // Handle as an operator
    if (_expr.length > 0 && operators.contains(_expr[_expr.length - 1])) {
      _expr = _expr.substring(0, _expr.length - 1);
    }
    _expr += key;
  } else if (digits.contains(key)) {
    // Handle as an operand
    _expr += key;
  } else if (key == 'C') {
    // Delete last character
    if (_expr.length > 0) {
      _expr = _expr.substring(0, _expr.length - 1);
    }
  } else if (key == '=') {
    try {
      var parser = const Parser();
      _result = parser.parseExpression(_expr).toString();
    } on Error {
      _result = 'Error';
    }
  }
  // ignore: invalid_use_of_protected_member
  _displayState.setState(() {
    _displayState._expression = _expr;
    _displayState._result = _result;
  });
}

class Keyboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new Expanded(
        flex: 2,
        child: new Center(
            child:
            new AspectRatio(
              aspectRatio: 1.0, // To center the GridView
              child: new GridView.count(
                crossAxisCount: 4,
                childAspectRatio: 1.0,
                padding: const EdgeInsets.all(1.0),
                mainAxisSpacing: 1.0,
                crossAxisSpacing: 1.0,
                children: [
                  // @formatter:off
                  '7', '8', '9', 'X',
                  '4', '5', '6', 'E',
                  '1', '2', '3', '-',
                  '0', '00', '.', 'C',
                  /*
                  '7', '8', '9', '/',
                  '4', '5', '6', '*',
                  '1', '2', '3', '-',
                  'C', '0', '=', '+',

                   */
                  // @formatter:on
                ].map((key) {
                  return new GridTile(
                    child: new KeyboardKey(key),
                  );
                }).toList(),
              ),
            )
        ));
  }
}

class KeyboardKey extends StatelessWidget {
  KeyboardKey(this._keyValue);

  final _keyValue;

  @override
  Widget build(BuildContext context) {
    return new FlatButton(
      child: new Text(
        _keyValue,
        style: new TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 26.0,
          color: Colors.black,
        ),
      ),
      color: Theme
          .of(context)
          .scaffoldBackgroundColor,
      onPressed: () {
        _addKey(_keyValue);
      },
    );
  }
}