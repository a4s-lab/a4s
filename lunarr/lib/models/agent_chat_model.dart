import 'package:lunarr/models/agent_card_model.dart';

enum AgentChatType { question, selection, thinking, answer }

class AgentChatModel {
  final AgentChatType type;
  final String? questionBody;
  final List<AgentCardModel>? selectionBody;
  final Object? thinkingBody;
  final String? answerBody;

  AgentChatModel.question(this.questionBody)
    : type = AgentChatType.question,
      selectionBody = null,
      thinkingBody = null,
      answerBody = null;

  static AgentChatModel questionExample() => AgentChatModel.question(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  );

  AgentChatModel.selection(this.selectionBody)
    : type = AgentChatType.selection,
      questionBody = null,
      thinkingBody = null,
      answerBody = null;

  static AgentChatModel selectionExample() => AgentChatModel.selection([
    AgentCardModel.seungho(true),
    AgentCardModel.kyungho(true),
    AgentCardModel.minseok(true),
    AgentCardModel.seungho(true),
  ]);

  AgentChatModel.thinking(this.thinkingBody)
    : type = AgentChatType.thinking,
      questionBody = null,
      selectionBody = null,
      answerBody = null;

  static AgentChatModel thinkingExample() => AgentChatModel.thinking(null);

  AgentChatModel.answer(this.answerBody)
    : type = AgentChatType.answer,
      selectionBody = null,
      questionBody = null,
      thinkingBody = null;

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
