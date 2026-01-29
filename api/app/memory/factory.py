from app.config import Config, MemoryProvider
from app.config import config as default_config
from app.memory.manager import MemoryManager


async def create_memory_manager(config: Config | None = None) -> MemoryManager:
    """Create a memory manager based on the configured provider.

    Args:
        config: Optional configuration. Uses default config if not provided.

    Returns:
        A configured MemoryManager instance.
    """
    cfg = config or default_config

    if cfg.memory_provider == MemoryProvider.GRAPHITI:
        from app.memory.graphiti_manager import GraphitiMemoryManager  # noqa: PLC0415

        return await GraphitiMemoryManager.create(cfg)
    if cfg.memory_provider == MemoryProvider.MEM0:
        from app.memory.mem0_manager import Mem0MemoryManager  # noqa: PLC0415

        return await Mem0MemoryManager.create(cfg)
    raise ValueError(f"Unsupported memory provider: {cfg.memory_provider}")
