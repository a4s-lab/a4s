# A4S MCP

MCP server for A4S agent orchestration. Enables agent discovery, A2A communication, and skill management.

Set `API_BASE_URL` to configure the A4S API endpoint (default: `http://localhost:8000`).

## Usage

### Google ADK

```python
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["run", "-m", "a4s_mcp"],
            env={"API_BASE_URL": "http://localhost:8000"},
        ),
        timeout=180,
    ),
    tool_filter=["search_agents", "send_a2a_message"],
)
```

### Claude Desktop

```json
{
  "mcpServers": {
    "a4s": {
      "command": "uv",
      "args": ["run", "-m", "a4s_mcp"],
      "cwd": "/path/to/a4s/mcp",
      "env": { "API_BASE_URL": "http://localhost:8000" }
    }
  }
}
```

## Tools

| Tool                                  | Description                   |
| ------------------------------------- | ----------------------------- |
| `search_agents(query, limit=10)`      | Find agents by capability     |
| `send_a2a_message(agent_id, message)` | Send message to agent via A2A |
| `search_skills(query, limit=10)`      | Find skills by description    |
| `get_skills(names)`                   | Get skills by exact name      |

## Resources

- `skill://{name}/instructions` - Skill instructions
- `skill://{name}/file/{path}` - Skill files

## Prompts

- `activate_skill(skill_name)` - Generate skill activation instructions
- `discover_skills(task_description)` - Recommend skills for a task
