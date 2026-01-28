from datetime import datetime
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Query, Request, Response
from pydantic import BaseModel, Field

from app.skills.models import Skill, SkillFile

if TYPE_CHECKING:
    from app.skills.registry import SkillsRegistry

router = APIRouter(prefix="/skills", tags=["skills"])


class RegisterSkillRequest(BaseModel):
    """Request body for registering a skill."""

    name: str = Field(description="Unique name for the skill (lowercase alphanumeric with hyphens).")
    description: str = Field(description="Description of the skill (1-1024 characters).")
    body: str = Field(default="", description="Skill instructions/content.")
    license: str | None = Field(default=None, description="License information.")
    compatibility: str | None = Field(default=None, description="Compatibility notes (max 500 characters).")
    tags: dict[str, str] = Field(default_factory=dict, description="Metadata tags.")
    allowed_tools: list[str] = Field(default_factory=list, description="List of allowed tools.")


class RegisterSkillFileRequest(BaseModel):
    """Request body for registering a skill file."""

    path: str = Field(description="File path within the skill.")
    content: bytes = Field(description="File content (base64 encoded in JSON).")


class SkillResponse(BaseModel):
    """Response model for a skill."""

    id: int
    name: str
    description: str
    body: str
    license: str | None
    compatibility: str | None
    tags: dict[str, str]
    allowed_tools: list[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_skill(cls, skill: Skill) -> "SkillResponse":
        return cls(
            id=skill.id,
            name=skill.name,
            description=skill.description,
            body=skill.body,
            license=skill.license,
            compatibility=skill.compatibility,
            tags=skill.tags,
            allowed_tools=skill.allowed_tools,
            created_at=skill.created_at,
            updated_at=skill.updated_at,
        )


class SkillListResponse(BaseModel):
    """Response for listing skills."""

    skills: list[SkillResponse]
    offset: int
    limit: int


class SkillSearchResponse(BaseModel):
    """Response for searching skills."""

    skills: list[SkillResponse]
    query: str
    limit: int


class SkillFileResponse(BaseModel):
    """Response model for a skill file (without content)."""

    id: int
    skill_id: int
    path: str
    created_at: datetime

    @classmethod
    def from_skill_file(cls, skill_file: SkillFile) -> "SkillFileResponse":
        return cls(
            id=skill_file.id,
            skill_id=skill_file.skill_id,
            path=skill_file.path,
            created_at=skill_file.created_at,
        )


class SkillFilesResponse(BaseModel):
    """Response for listing skill files."""

    files: list[SkillFileResponse]
    skill_id: int


@router.post("", status_code=201)
async def register_skill(request: Request, body: RegisterSkillRequest) -> SkillResponse:
    """Register a skill in the registry.

    Args:
        request: FastAPI request object.
        body: Skill registration details.

    Returns:
        The registered skill.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry

    skill = Skill(
        name=body.name,
        description=body.description,
        body=body.body,
        license=body.license,
        compatibility=body.compatibility,
        tags=body.tags,
        allowed_tools=body.allowed_tools,
    )
    registered = await skills_registry.register_skill(skill)
    return SkillResponse.from_skill(registered)


@router.delete("/{skill_id}", status_code=204)
async def unregister_skill(request: Request, skill_id: int) -> None:
    """Unregister a skill from the registry.

    Args:
        request: FastAPI request object.
        skill_id: ID of the skill to unregister.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    await skills_registry.unregister_skill(skill_id)


@router.get("")
async def list_skills(
    request: Request,
    offset: Annotated[int, Query(ge=0, description="Number of skills to skip.")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Maximum number of skills to return.")] = 50,
) -> SkillListResponse:
    """List skills with pagination.

    Args:
        request: FastAPI request object.
        offset: Number of skills to skip.
        limit: Maximum number of skills to return.

    Returns:
        Paginated list of skills.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    skills = await skills_registry.list_skills(offset=offset, limit=limit)
    return SkillListResponse(
        skills=[SkillResponse.from_skill(s) for s in skills],
        offset=offset,
        limit=limit,
    )


@router.get("/search")
async def search_skills(
    request: Request,
    query: Annotated[str, Query(description="Search query.")],
    limit: Annotated[int, Query(ge=1, le=100, description="Maximum number of results.")] = 10,
) -> SkillSearchResponse:
    """Search skills by query.

    Args:
        request: FastAPI request object.
        query: Search query string.
        limit: Maximum number of results.

    Returns:
        Matching skills.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    skills = await skills_registry.search_skills(query, limit=limit)
    return SkillSearchResponse(
        skills=[SkillResponse.from_skill(s) for s in skills],
        query=query,
        limit=limit,
    )


@router.get("/by-name/{name}")
async def get_skill_by_name(request: Request, name: str) -> SkillResponse:
    """Get a skill by name.

    Args:
        request: FastAPI request object.
        name: Name of the skill to retrieve.

    Returns:
        The skill.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    skill = await skills_registry.get_skill_by_name(name)
    return SkillResponse.from_skill(skill)


@router.get("/{skill_id}")
async def get_skill(request: Request, skill_id: int) -> SkillResponse:
    """Get a skill by ID.

    Args:
        request: FastAPI request object.
        skill_id: ID of the skill to retrieve.

    Returns:
        The skill.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    skill = await skills_registry.get_skill(skill_id)
    return SkillResponse.from_skill(skill)


@router.get("/{skill_id}/files")
async def get_skill_files(request: Request, skill_id: int) -> SkillFilesResponse:
    """Get all files for a skill.

    Args:
        request: FastAPI request object.
        skill_id: ID of the skill.

    Returns:
        List of skill files (metadata only).
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    files = await skills_registry.get_skill_files(skill_id)
    return SkillFilesResponse(
        files=[SkillFileResponse.from_skill_file(f) for f in files],
        skill_id=skill_id,
    )


@router.get("/{skill_id}/files/{path:path}")
async def get_skill_file(request: Request, skill_id: int, path: str) -> Response:
    """Get a specific file for a skill.

    Args:
        request: FastAPI request object.
        skill_id: ID of the skill.
        path: Path of the file within the skill.

    Returns:
        The file content as raw bytes.
    """
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    skill_file = await skills_registry.get_skill_file_by_path(skill_id, path)
    return Response(content=skill_file.content, media_type="application/octet-stream")
