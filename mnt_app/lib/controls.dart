import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class ControlsWidget extends StatefulWidget {
  const ControlsWidget({super.key});
  @override
  _ControlsWidgetState createState() => _ControlsWidgetState();
}

class _ControlsWidgetState extends State<ControlsWidget> {
  bool _on = true;
  int _move = 50;

  void _toggleOn() {
    setState(() {
      if (_on) {
        _move -= 1;
        _on = false;
      } else {
        _move += 1;
        _on = true;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          padding: const EdgeInsets.all(0),
          child: IconButton(
            padding: const EdgeInsets.all(0),
            alignment: Alignment.centerRight,
            icon:
                (_on ? const Icon(Icons.star) : const Icon(Icons.star_border)),
            color: Colors.red[500],
            onPressed: _toggleOn,
          ),
        ),
        SizedBox(
          width: 18,
          child: SizedBox(
            child: Text('$_move'),
          ),
        ),
      ],
    );
  }
}
