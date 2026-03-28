# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- ## 🔍 LMS Health Check Report

**System Status:** ❌ **UNHEALTHY**

### Findings

| Metric | Value |
|--------|-------|
| LMS Backend Status | HTTP 404 (unhealthy) |
| Errors (last 2 min) | 2 |
| Item Count | Unknown |

### Root Cause

**Database connection failure** — DNS resolution error

**Log Evidence:**
- **Time:** 2026-03-28T16:47:36Z
- **Error:** `[Errno -2] Name or service not known`
- **Operation:** `db_query` (SELECT on `item` table)
- **Trace ID:** `59a828084b98503c66cde7b0933f5c6d`

**Trace Analysis:**
- The `GET /items/` request failed during the `connect` operation
- Connection attempt duration: 392ms (timed out/failed)
- The database hostname cannot be resolved

### Impact
- LMS API endpoints returning errors
- Database queries failing due to DNS resolution issue
- Item data inaccessible

### Recommended Action
Check database connection configuration and DNS settings for the LMS backend service. -->

## Task 4C — Bug fix and recovery

<!--
    ## Root Cause
    **Database connection failure** — The LMS backend cannot connect to its     
    PostgreSQL database due to a DNS resolution error.

    ## Evidence

    **Log Evidence (from the last 10 minutes):**
    - **Timestamp:** `2026-03-28T16:56:06Z`
    - **Error:** `[Errno -2] Name or service not known`
    - **Operation:** `db_query` (SELECT on `item` table)
    - **Affected endpoint:** `GET /items/` → returned HTTP 500
    - **Trace ID:** `c1a6f087c9eb604d1fe7ab328fd398f5`

    **Error Count:** 5 errors in the last 10 minutes, all with the same DNS     
    resolution failure.

    ## What Failed
    1. The LMS service attempted to query the `item` table in PostgreSQL        
    2. The database hostname could not be resolved (DNS failure)
    3. The `GET /items/` request failed with HTTP 500
    4. This blocks all lab-related queries (including the list of available labs)

    ## Affected Service
    - **Service:** Learning Management Service (`lms_backend`)
    - **Failing operation:** Database query during items list retrieval
    - **Impact:** Users cannot view labs, scores, or any LMS data

    ## Likely Cause
    The database service hostname in the LMS configuration is either:
    - Misspelled or incorrect
    - The database container/service is not running
    - Network/DNS service discovery is broken in the deployment environment     

    Would you like me to trigger the LMS sync pipeline to attempt recovery, or do
     you 🐾 **Health Check Report**
     4. 🐾 **Health Check Report**

✅ **System Status: Healthy**

- **Errors (last 2 min):** 0
- **LMS Backend:** Healthy
- **Item Count:** 56

No issues detected. All systems operational. -->
