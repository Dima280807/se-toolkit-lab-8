"""MCP server exposing VictoriaLogs and VictoriaTraces as tools."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel


class LogsSearchParams(BaseModel):
    query: str = "severity:ERROR"
    limit: int = 10


class LogsErrorCountParams(BaseModel):
    service: str = "Learning Management Service"
    minutes: int = 60


class TracesListParams(BaseModel):
    service: str = "Learning Management Service"
    limit: int = 5


class TracesGetParams(BaseModel):
    trace_id: str


def _text(data: Any) -> list[TextContent]:
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


def create_server(victorialogs_url: str, victoriatraces_url: str) -> Server:
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="logs_search",
                description="Search logs in VictoriaLogs by query. Use LogsQL syntax. Common queries: 'severity:ERROR', 'service.name:\"Learning Management Service\"', '_time:10m severity:ERROR'",
                inputSchema=LogsSearchParams.model_json_schema(),
            ),
            Tool(
                name="logs_error_count",
                description="Count errors per service over a time window in VictoriaLogs",
                inputSchema=LogsErrorCountParams.model_json_schema(),
            ),
            Tool(
                name="traces_list",
                description="List recent traces for a service from VictoriaTraces",
                inputSchema=TracesListParams.model_json_schema(),
            ),
            Tool(
                name="traces_get",
                description="Get a specific trace by ID from VictoriaTraces",
                inputSchema=TracesGetParams.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        try:
            if name == "logs_search":
                args = LogsSearchParams.model_validate(arguments or {})
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        f"{victorialogs_url}/select/logsql/query",
                        params={"query": args.query, "limit": args.limit},
                        timeout=30,
                    )
                    resp.raise_for_status()
                    return _text({"logs": resp.text.splitlines()[:args.limit]})

            elif name == "logs_error_count":
                args = LogsErrorCountParams.model_validate(arguments or {})
                query = f'_time:{args.minutes}m service.name:"{args.service}" severity:ERROR'
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        f"{victorialogs_url}/select/logsql/query",
                        params={"query": query, "limit": 1000},
                        timeout=30,
                    )
                    resp.raise_for_status()
                    lines = resp.text.splitlines()
                    return _text({"count": len(lines), "service": args.service, "minutes": args.minutes})

            elif name == "traces_list":
                args = TracesListParams.model_validate(arguments or {})
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"{victoriatraces_url}/select/jaeger/api/traces",
                        params={"service": args.service, "limit": args.limit},
                        timeout=30,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    traces = data.get("data", [])
                    summary = [
                        {
                            "trace_id": t.get("traceID"),
                            "spans": len(t.get("spans", [])),
                        }
                        for t in traces
                    ]
                    return _text({"traces": summary})

            elif name == "traces_get":
                args = TracesGetParams.model_validate(arguments or {})
                async with httpx.AsyncClient() as client:
                    resp = await client.get(
                        f"{victoriatraces_url}/select/jaeger/api/traces/{args.trace_id}",
                        timeout=30,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    traces = data.get("data", [])
                    if traces:
                        trace = traces[0]
                        spans = [
                            {
                                "operation": s.get("operationName"),
                                "duration_us": s.get("duration"),
                                "service": trace.get("processes", {}).get(s.get("processID"), {}).get("serviceName"),
                            }
                            for s in trace.get("spans", [])
                        ]
                        return _text({"trace_id": args.trace_id, "spans": spans})
                    return _text({"error": "Trace not found"})

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    import os

    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:9428")
    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:10428")

    server = create_server(victorialogs_url, victoriatraces_url)
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
