import 'package:flutter/material.dart';

class AgentModel {
  AgentModel(this.iconString, this.labelString);

  final String iconString;
  final String labelString;

  // Widget getIcon(double radius) =>
  //     CircleAvatar(radius: radius, child: Image.network(iconString));
  Widget getIcon(double radius) =>
      CircleAvatar(radius: radius, child: Image.asset(iconString));

  static AgentModel seungho() =>
      AgentModel('assets/avatars/1.png', 'Seungho\'s Agent');
  static AgentModel kyungho() =>
      AgentModel('assets/avatars/2.png', 'Kyungho\'s Agent');
  static AgentModel minseok() =>
      AgentModel('assets/avatars/4.png', 'Minseok\'s Agent');
}
