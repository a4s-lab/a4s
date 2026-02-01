class WorkspaceService {
  WorkspaceService._internal();

  static final WorkspaceService _instance = WorkspaceService._internal();

  factory WorkspaceService() => _instance;
}
