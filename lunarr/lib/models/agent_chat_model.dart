import 'package:lunarr/models/agent_card_model.dart';

enum AgentChatType { question, selection, thinking, answer }

class AgentChatModel {
  final AgentChatType agentChatType;
  final String? body;
  final List<AgentCardModel>? agentCardModels;

  AgentChatModel.question(this.body)
    : agentChatType = AgentChatType.question,
      agentCardModels = null;

  static AgentChatModel questionExample() => AgentChatModel.question(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  );

  AgentChatModel.selection(this.agentCardModels)
    : agentChatType = AgentChatType.selection,
      body = null;

  static AgentChatModel selectionExample() => AgentChatModel.selection([
    AgentCardModel.seungho(true),
    AgentCardModel.kyungho(true),
    AgentCardModel.minseok(true),
    AgentCardModel.seungho(true),
  ]);

  AgentChatModel.thinking()
    : agentChatType = AgentChatType.thinking,
      body = null,
      agentCardModels = null;

  static AgentChatModel thinkingExample() => AgentChatModel.thinking();

  AgentChatModel.answer(this.body)
    : agentChatType = AgentChatType.answer,
      agentCardModels = null;

  static AgentChatModel answerExample() => AgentChatModel.answer('''
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
''');

  static List<AgentChatModel> examples() => [
    AgentChatModel.questionExample(),
    AgentChatModel.selectionExample(),
    AgentChatModel.thinkingExample(),
    AgentChatModel.answerExample(),
  ];
}
