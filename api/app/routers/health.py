import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from qdrant_client.http.exceptions import UnexpectedResponse

if TYPE_CHECKING:
    from app.broker.registry import AgentRegistry
    from app.runtime.manager import RuntimeManager
    from app.skills.registry import SkillsRegistry

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/livez")
async def liveness() -> dict[str, str]:
    """Liveness check.

    Returns:
        Simple status indicating the service is alive.
    """
    return {"status": "ok"}


@router.get("/readyz")
async def readiness(request: Request) -> JSONResponse:
    """Readiness check.

    Checks connectivity to its dependencies such as agent registry, skills registry, and runtime manager.

    Returns:
        Status of each dependency and overall readiness.
    """
    registry: AgentRegistry = request.app.state.registry
    skills_registry: SkillsRegistry = request.app.state.skills_registry
    runtime_manager: RuntimeManager = request.app.state.runtime_manager

    checks: dict[str, bool] = {}
    errors: dict[str, str] = {}

    try:
        await registry.list_agents(limit=1)
        checks["agent_registry"] = True
    except UnexpectedResponse as e:
        checks["agent_registry"] = False
        errors["agent_registry"] = str(e)
        logger.warning("Agent registry health check failed: %s", e)
    except Exception as e:
        checks["agent_registry"] = False
        errors["agent_registry"] = str(e)
        logger.warning("Agent registry health check failed: %s", e)

    try:
        await skills_registry.list_skills(limit=1)
        checks["skills_registry"] = True
    except Exception as e:
        checks["skills_registry"] = False
        errors["skills_registry"] = str(e)
        logger.warning("Skills registry health check failed: %s", e)

    try:
        runtime_manager.list_agents()
        checks["runtime_manager"] = True
    except Exception as e:
        checks["runtime_manager"] = False
        errors["runtime_manager"] = str(e)
        logger.warning("Runtime manager health check failed: %s", e)

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    response = {
        "status": "ok" if all_healthy else "degraded",
        "checks": checks,
    }
    if errors:
        response["errors"] = errors

    return JSONResponse(content=response, status_code=status_code)
