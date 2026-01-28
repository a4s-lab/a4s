from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from a4s_mcp.config import config


@dataclass
class AppContext:
    """Application context shared across MCP tools."""

    client: httpx.AsyncClient


@asynccontextmanager
async def mcp_lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    async with httpx.AsyncClient(base_url=config.api_base_url) as client:
        yield AppContext(client=client)


mcp = FastMCP("A4S MCP Server", lifespan=mcp_lifespan)


@mcp.tool()
async def search_agents(
    ctx: Context[ServerSession, AppContext],
    query: str,
    limit: int = 10,
) -> dict:
    """Search for agents by name/description.

    When to use:
    - Find agents by capability (query="code review")

    Args:
        query: Search query.
        limit: Max results to return (default 10).

    Returns:
        {agents, query, limit}
    """
    client = ctx.request_context.lifespan_context.client
    resp = await client.get("/api/v1/agents/search", params={"query": query, "limit": limit})
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
async def get_skills(
    ctx: Context[ServerSession, AppContext],
    names: list[str],
) -> dict:
    """Get metadata for specific skills by exact name.

    When to use:
    - Retrieve skills by name after search
    - Verify skills exist before activation

    When NOT to use:
    - Don't know names - use search_skills
    - Need instructions - read skill://{name}/instructions

    Args:
        names: List of exact skill names to retrieve.

    Returns:
        {found: [{name, description}], not_found: [names]}
    """
    client = ctx.request_context.lifespan_context.client
    found = []
    not_found = []

    for name in names:
        resp = await client.get(f"/api/v1/skills/by-name/{name}")
        if resp.status_code == 200:
            skill = resp.json()
            found.append({"name": skill["name"], "description": skill["description"]})
        else:
            not_found.append(name)

    return {"found": found, "not_found": not_found}


@mcp.tool()
async def search_skills(
    ctx: Context[ServerSession, AppContext],
    query: str,
    limit: int = 10,
) -> dict:
    """Search for skills by name/description.

    When to use:
    - Find skills for a task (query="create PDF documents")

    When NOT to use:
    - Know exact skill names - use get_skills
    - Need full instructions - read skill://{name}/instructions

    Args:
        query: Search query.
        limit: Max results to return (default 10).

    Returns:
        {skills, query, limit}
    """
    client = ctx.request_context.lifespan_context.client
    resp = await client.get("/api/v1/skills/search", params={"query": query, "limit": limit})
    resp.raise_for_status()
    data = resp.json()
    return {
        "skills": [{"name": s["name"], "description": s["description"]} for s in data["skills"]],
        "query": query,
        "limit": limit,
    }


@mcp.resource("skill://{skill_name}/instructions")
async def get_skill_instructions(skill_name: str) -> str:
    """Get the SKILL.md instructions for a skill.

    Returns the full body content of the skill's SKILL.md file,
    which contains detailed instructions for using the skill.
    """
    async with httpx.AsyncClient(base_url=config.api_base_url) as client:
        resp = await client.get(f"/api/v1/skills/by-name/{skill_name}")
        resp.raise_for_status()
        skill = resp.json()
        return skill["body"]


@mcp.resource("skill://{skill_name}/file/{path}")
async def get_skill_file(skill_name: str, path: str) -> bytes:
    """Get a specific file associated with a skill.

    Returns the content of the specified file from the skill's
    associated files (scripts, references, assets, etc.).
    """
    async with httpx.AsyncClient(base_url=config.api_base_url) as client:
        resp = await client.get(f"/api/v1/skills/by-name/{skill_name}")
        resp.raise_for_status()
        skill = resp.json()
        skill_id = skill["id"]

        resp = await client.get(f"/api/v1/skills/{skill_id}/files/{path}")
        resp.raise_for_status()
        return resp.content


@mcp.prompt()
async def activate_skill(skill_name: str) -> str:
    """Generate instructions for activating and using a specific skill.

    Args:
        skill_name: Name of the skill to activate.

    Returns:
        Formatted prompt with skill instructions.
    """
    async with httpx.AsyncClient(base_url=config.api_base_url) as client:
        resp = await client.get(f"/api/v1/skills/by-name/{skill_name}")
        if resp.status_code != 200:
            return f"Error: Skill '{skill_name}' not found. Use search_skills to find available skills."

        skill = resp.json()

    parts = [f"# Skill: {skill['name']}", "", "## Description", skill["description"], ""]

    if skill.get("compatibility"):
        parts.extend(["## Compatibility", skill["compatibility"], ""])

    if skill.get("allowed_tools"):
        parts.extend(["## Allowed Tools", ", ".join(skill["allowed_tools"]), ""])

    if skill.get("body"):
        parts.extend(["## Instructions", skill["body"], ""])

    parts.extend(["---", "You are now operating with this skill activated. Follow the instructions above."])

    return "\n".join(parts)


@mcp.prompt()
async def discover_skills(task_description: str, limit: int = 5) -> str:
    """Find and recommend skills for a given task.

    Args:
        task_description: Description of the task to accomplish.
        limit: Maximum number of skills to recommend.

    Returns:
        Formatted prompt with skill recommendations.
    """
    async with httpx.AsyncClient(base_url=config.api_base_url) as client:
        resp = await client.get("/api/v1/skills/search", params={"query": task_description, "limit": limit})
        resp.raise_for_status()
        data = resp.json()
        skills = data["skills"]

    if not skills:
        return (
            f"No skills found matching: {task_description}\n\n"
            "Consider trying a broader search query with search_skills."
        )

    parts = [
        "# Skill Discovery Results",
        "",
        f"Task: {task_description}",
        "",
        f"Found {len(skills)} relevant skill(s):",
        "",
    ]

    for i, skill in enumerate(skills, 1):
        parts.extend([f"## {i}. {skill['name']}", skill["description"], ""])
        if skill.get("tags"):
            tags_str = ", ".join(f"{k}={v}" for k, v in skill["tags"].items())
            parts.extend([f"Tags: {tags_str}", ""])

    parts.extend(
        [
            "---",
            "To activate a skill, use the activate_skill prompt with the skill name.",
            "To get more details, read its instructions: skill://{skill_name}/instructions",
        ]
    )

    return "\n".join(parts)
