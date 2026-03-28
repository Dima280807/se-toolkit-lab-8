"""MCP observability server entry point for python -m execution."""

from mcp_obs.server import main

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
