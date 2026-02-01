import 'package:flutter/material.dart';

class ChannelModel {
  ChannelModel(this.iconString, this.labelString, this.agentsCount);

  final String iconString;
  final String labelString;
  final int agentsCount;

  // Widget get icon => CircleAvatar(child: Image.network(iconString));
  Widget getIcon(double radius) => CircleAvatar(
    radius: radius,
    backgroundColor: Colors.transparent,
    child: Text('#'),
  );

  static ChannelModel all() => ChannelModel('', 'All', 20);
  static ChannelModel frontendTeam() => ChannelModel('', 'Frontend Team', 5);
  static ChannelModel backendTeam() => ChannelModel('', 'Backend Team', 5);
  static ChannelModel developers() => ChannelModel('', 'Developers', 10);
  static ChannelModel lunchGroup() => ChannelModel('', 'Lunch Group', 3);
}
