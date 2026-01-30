import 'package:flutter/material.dart';

class ChannelModel {
  ChannelModel(this.iconString, this.labelString);

  String iconString;
  String labelString;

  // Widget get icon => CircleAvatar(child: Image.network(iconString));
  Widget getIcon(double radius) => CircleAvatar(
    radius: radius,
    backgroundColor: Colors.transparent,
    child: Text('#'),
  );
  Widget get label => Text(labelString);
}
