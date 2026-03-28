---
name: observability
description: Use observability MCP tools to query logs and traces
always: true
---

# Observability Skill

Use observability MCP tools to answer questions about system health, errors, and failures.

## Available Tools

- `logs_search` — Search logs in VictoriaLogs by query using LogsQL syntax
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service from VictoriaTraces
- `traces_get` — Get a specific trace by ID from VictoriaTraces

## Strategy

### When the user asks about errors or system health:

1. **Start with `logs_error_count`** to see if there are recent errors
   - Use a narrow time window (e.g., 10 minutes) for recent issues
   - Specify the service name (e.g., "Learning Management Service")

2. **If errors exist, use `logs_search`** to inspect the error details
   - Query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
   - Look for `trace_id` in the error logs

3. **If a trace_id is found, use `traces_get`** to inspect the full trace
   - This shows the span hierarchy and where the failure occurred

4. **Summarize findings concisely** — don't dump raw JSON
   - Report: what failed, when, which service, any trace information
   - Keep responses brief and actionable

### Common Queries

**"Any errors in the last hour?"**
→ Call `logs_error_count` with `minutes: 60`

**"What went wrong with the last request?"**
→ Call `logs_search` with `_time:5m severity:ERROR`, then `traces_get` if trace_id found

**"Show me recent traces"**
→ Call `traces_list` with the service name

### LogsQL Query Examples

- `_time:10m severity:ERROR` — Errors in last 10 minutes
- `service.name:"Learning Management Service" severity:ERROR` — Errors for specific service
- `_time:1h service.name:"Learning Management Service"` — All logs for service in last hour
- `trace_id:ead6ea3d2412a724a4f8f7e02ce10121` — Logs for specific trace

### Response Style

- Keep responses concise — summarize key findings
- Use bullet points for multiple data points
- When reporting errors, include: timestamp, service, error message, trace_id (if available)
- When reporting trace analysis, include: span hierarchy, which span failed, duration

## Examples

**User:** "Any LMS backend errors in the last 10 minutes?"
**You:** Call `logs_error_count` with service="Learning Management Service", minutes=10. If count > 0, call `logs_search` to get details.

**User:** "What happened with trace abc123?"
**You:** Call `traces_get` with trace_id="abc123" and summarize the span hierarchy.

**User:** "Is the system healthy?"
**You:** Call `logs_error_count` for recent errors. If none, report healthy. If errors exist, investigate with `logs_search`.
