import 'dart:async';

import 'package:flutter/material.dart';
import 'package:lunarr/models/agent_chat_model.dart';

class AgentChatController {
  bool _lock = false;
  final List<AgentChatModel> _agentChatModels = [];
  final TextEditingController _textEditingController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  String input = '';
  String _input = '';

  bool get lock => _lock;
  List<AgentChatModel> get agentChatModels => _agentChatModels;
  TextEditingController get textEditingController => _textEditingController;
  ScrollController get scrollController => _scrollController;

  void scroll() {
    Timer(const Duration(milliseconds: 300), () {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  // TODO: integrate API (not for now)
  Future<void> fetchAgentChatModels() async {
    await Future.delayed(const Duration(seconds: 1));
    List<AgentChatModel> agentChatModels = [
      ...AgentChatModel.examples(),
      ...AgentChatModel.examples(),
      ...AgentChatModel.examples(),
      ...AgentChatModel.examples(),
    ];

    _agentChatModels.addAll(agentChatModels);
    scroll();
  }

  void addQuestion() {
    if (input.isEmpty) return;
    _lock = true;

    _input = input;
    input = '';
    _textEditingController.clear();

    _agentChatModels.add(AgentChatModel.question(_input));
    scroll();
  }

  // TODO: integrate API
  Future<void> addSelection() async {
    await Future.delayed(const Duration(seconds: 1));
    AgentChatModel selection = AgentChatModel.selectionExample();

    _agentChatModels.add(selection);
    scroll();
  }

  // TODO: integrate API (not for now)
  Future<void> addThinking() async {
    await Future.delayed(const Duration(seconds: 1));
    AgentChatModel thinking = AgentChatModel.thinkingExample();

    _agentChatModels.add(thinking);
    scroll();
  }

  // TODO: integrate API
  Future<void> addAnswer() async {
    await Future.delayed(const Duration(seconds: 1));
    AgentChatModel answer = AgentChatModel.answerExample();

    _agentChatModels.add(answer);
    scroll();

    _lock = false;
  }
}
