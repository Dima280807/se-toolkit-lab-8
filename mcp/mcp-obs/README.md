# MCP Observability Server

MCP server that exposes VictoriaLogs and VictoriaTraces as tools for AI agents.

## Tools

- `logs_search` — Search logs in VictoriaLogs by query using LogsQL syntax
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service
- `traces_get` — Get a specific trace by ID

## Usage

```bash
NANOBOT_VICTORIALOGS_URL=http://localhost:9428 \
NANOBOT_VICTORIATRACES_URL=http://localhost:10428 \
uv run python -m mcp_obs
```

## Environment Variables

- `NANOBOT_VICTORIALOGS_URL` — VictoriaLogs base URL (default: http://localhost:9428)
- `NANOBOT_VICTORIATRACES_URL` — VictoriaTraces base URL (default: http://localhost:10428)
