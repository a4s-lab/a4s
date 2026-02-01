class SignServices {
  SignServices._internal();

  static final SignServices _instance = SignServices._internal();

  factory SignServices() => _instance;

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
