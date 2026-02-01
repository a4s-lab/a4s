import 'package:lunarr/models/agent_card_model.dart';

enum ChannelChatType { question, selection, thinking, answer }

class ChannelChatModel {
  final ChannelChatType type;
  final String? questionBody;
  final List<AgentCardModel>? selectionBody;
  final Object? thinkingBody;
  final String? answerBody;

  ChannelChatModel.question(this.questionBody)
    : type = ChannelChatType.question,
      selectionBody = null,
      thinkingBody = null,
      answerBody = null;

  static ChannelChatModel questionExample() => ChannelChatModel.question(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  );

  ChannelChatModel.selection(this.selectionBody)
    : type = ChannelChatType.selection,
      questionBody = null,
      thinkingBody = null,
      answerBody = null;

  static ChannelChatModel selectionExample() => ChannelChatModel.selection([
    AgentCardModel.seungho(true),
    AgentCardModel.kyungho(true),
    AgentCardModel.minseok(true),
    AgentCardModel.seungho(true),
  ]);

  ChannelChatModel.thinking(this.thinkingBody)
    : type = ChannelChatType.thinking,
      questionBody = null,
      selectionBody = null,
      answerBody = null;

  static ChannelChatModel thinkingExample() => ChannelChatModel.thinking(null);

  ChannelChatModel.answer(this.answerBody)
    : type = ChannelChatType.answer,
      selectionBody = null,
      questionBody = null,
      thinkingBody = null;

  static ChannelChatModel answerExample() => ChannelChatModel.answer('''
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
''');

  static List<ChannelChatModel> examples() => [
    ChannelChatModel.questionExample(),
    ChannelChatModel.selectionExample(),
    ChannelChatModel.thinkingExample(),
    ChannelChatModel.answerExample(),
  ];
}
