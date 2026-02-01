import 'package:flutter/material.dart';
import 'package:lunarr/constants/colors.dart';
import 'package:lunarr/services/agent_service.dart';
import 'package:lunarr/services/channel_service.dart';
import 'package:lunarr/views/main_view.dart';

class WorkspaceView extends StatefulWidget {
  const WorkspaceView({super.key});

  @override
  State<WorkspaceView> createState() => _WorkspaceViewState();
}

class _WorkspaceViewState extends State<WorkspaceView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: LUNARR_COLOR),
        child: Center(
          child: FilledButton(
            onPressed: () async {
              final navigator = Navigator.of(context);
              await ChannelService().fetchChannelModels();
              await AgentService().fetchAgentModels();
              navigator.pushReplacement(
                MaterialPageRoute(builder: (context) => MainView()),
              );
            },
            child: Text('C Company'),
          ),
        ),
      ),
    );
  }
}
