import 'package:flutter/material.dart';
import 'package:lunarr/services/channel_service.dart';

class ChannelChatView extends StatefulWidget {
  const ChannelChatView({super.key});

  @override
  State<ChannelChatView> createState() => _ChannelChatViewState();
}

class _ChannelChatViewState extends State<ChannelChatView> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Channel Chat View of ${ChannelService().channelModel!.labelString}',
      ),
    );
  }
}
