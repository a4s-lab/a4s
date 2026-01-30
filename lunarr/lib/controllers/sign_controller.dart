class SignController {
  SignController._internal();

  static final SignController _instance = SignController._internal();

  factory SignController() => _instance;

  String? signInEmailAddress;
  String? signInPassword;
  String? firstName;
  String? lastName;
  String? birthday;
  String? gender;
  String? signUpEmailAddress;
  String? signUpPassword;
  String? confirm;
  String? code;

  void clear() {
    signInEmailAddress = signInPassword = firstName = lastName = birthday =
        gender = signUpEmailAddress = signUpPassword = confirm = code = null;
  }
}
