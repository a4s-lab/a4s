class UserService {
  UserService._internal();

  static final UserService _instance = UserService._internal();

  factory UserService() => _instance;
}
