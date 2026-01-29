from __future__ import annotations

import logging

from mem0 import AsyncMemory

from app.config import Config
from app.config import config as default_config
from app.memory.config import to_mem0_config
from app.memory.manager import MemoryManager
from app.memory.models import (
    CreateMemoryRequest,
    Memory,
    QueuedMemoryResponse,
    SearchMemoryRequest,
    UpdateMemoryRequest,
)

logger = logging.getLogger(__name__)


class Mem0MemoryManager(MemoryManager):
    def __init__(self, memory: AsyncMemory) -> None:
        self.memory = memory

    @classmethod
    async def create(cls, config: Config | None = None) -> Mem0MemoryManager:
        """Create a new Mem0MemoryManager instance.

        Args:
            config: Optional configuration. Uses default config if not provided.

        Returns:
            A configured Mem0MemoryManager instance.
        """
        mem0_config = to_mem0_config(config or default_config)
        memory = await AsyncMemory.from_config(mem0_config)
        return cls(memory)

    def _build_agent_id_with_visibility(self, agent_id: str, visibility: str) -> str:
        return f"{agent_id}-{visibility}"

    def _get_search_agent_ids(self, agent_id: str, requester_id: str, owner_id: str) -> list[str]:
        if requester_id == owner_id:
            return [f"{agent_id}-private", f"{agent_id}-public"]
        return [f"{agent_id}-public"]

    async def add(
        self, request: CreateMemoryRequest, owner_id: str, requester_id: str
    ) -> Memory | QueuedMemoryResponse:
        """Add a new memory.

        Args:
            request: Memory creation request.
            owner_id: ID of the agent's owner.
            requester_id: ID of the requester.

        Returns:
            The created memory.

        Raises:
            PermissionError: If requester is not the owner.
        """
        if requester_id != owner_id:
            raise PermissionError("Only the owner can write to agent memory")

        scoped_agent_id = self._build_agent_id_with_visibility(request.agent_id, request.visibility.value)
        result = await self.memory.add(
            messages=request.messages,
            agent_id=scoped_agent_id,
            metadata=request.metadata,
        )
        mem = result["results"][0] if result.get("results") else {}
        return Memory(
            id=mem.get("id", ""),
            content=mem.get("memory", ""),
            metadata=mem.get("metadata"),
        )

    async def search(self, request: SearchMemoryRequest, owner_id: str, requester_id: str) -> list[Memory]:
        """Search for memories with access control.

        Args:
            request: Search request.
            owner_id: ID of the agent's owner.
            requester_id: ID of the requester for access control.

        Returns:
            List of matching memories based on access level.
        """
        agent_ids = self._get_search_agent_ids(request.agent_id, requester_id, owner_id)

        all_results: list[dict] = []
        for aid in agent_ids:
            try:
                results = await self.memory.search(
                    query=request.query,
                    agent_id=aid,
                    limit=request.limit,
                )
                all_results.extend(results.get("results", []))
            except Exception:
                logger.exception("Error searching memories for agent_id: %s", aid)

        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        all_results = all_results[: request.limit]

        return [
            Memory(
                id=r.get("id", ""),
                content=r.get("memory", ""),
                score=r.get("score"),
                metadata=r.get("metadata"),
            )
            for r in all_results
        ]

    async def update(self, memory_id: str, request: UpdateMemoryRequest) -> Memory:
        await self.memory.update(memory_id, request.content)
        return Memory(id=memory_id, content=request.content)

    async def delete(self, memory_id: str, owner_id: str, requester_id: str) -> None:
        """Delete a memory.

        Args:
            memory_id: ID of the memory to delete.
            owner_id: ID of the agent's owner.
            requester_id: ID of the requester.

        Raises:
            PermissionError: If requester is not the owner.
        """
        if requester_id != owner_id:
            raise PermissionError("Only the owner can delete agent memory")
        await self.memory.delete(memory_id)

    async def close(self) -> None:
        pass
