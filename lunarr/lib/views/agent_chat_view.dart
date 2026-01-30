import 'package:flutter/material.dart';
import 'package:lunarr/services/agent_service.dart';

class AgentChatView extends StatefulWidget {
  const AgentChatView({super.key});

  @override
  State<AgentChatView> createState() => _AgentChatViewState();
}

class _AgentChatViewState extends State<AgentChatView> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Agent Chat View of ${AgentService().agentModel!.labelString}',
      ),
    );
  }
}
