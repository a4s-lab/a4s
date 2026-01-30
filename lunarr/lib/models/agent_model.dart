import 'package:flutter/material.dart';

class AgentModel {
  AgentModel(this.iconString, this.labelString);

  String iconString;
  String labelString;

  // Widget getIcon(double radius) =>
  //     CircleAvatar(radius: radius, child: Image.network(iconString));
  Widget getIcon(double radius) => CircleAvatar(
    radius: radius,
    child: Image.asset('assets/avatars/$iconString.png'),
  );
  Widget get label => Text(labelString);
}
