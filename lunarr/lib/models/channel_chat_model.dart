import 'package:lunarr/models/agent_card_model.dart';

enum ChannelChatType { question, selection, thinking, answer }

class ChannelChatModel {
  final ChannelChatType channelChatType;
  final String? body;
  final List<AgentCardModel>? agentCardModels;

  ChannelChatModel.question(this.body)
    : channelChatType = ChannelChatType.question,
      agentCardModels = null;

  static ChannelChatModel questionExample() => ChannelChatModel.question(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  );

  ChannelChatModel.selection(this.agentCardModels)
    : channelChatType = ChannelChatType.selection,
      body = null;

  static ChannelChatModel selectionExample() => ChannelChatModel.selection([
    AgentCardModel.seungho(true),
    AgentCardModel.kyungho(true),
    AgentCardModel.minseok(true),
    AgentCardModel.seungho(true),
  ]);

  ChannelChatModel.thinking()
    : channelChatType = ChannelChatType.thinking,
      body = null,
      agentCardModels = null;

  static ChannelChatModel thinkingExample() => ChannelChatModel.thinking();

  ChannelChatModel.answer(this.body)
    : channelChatType = ChannelChatType.answer,
      agentCardModels = null;

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
