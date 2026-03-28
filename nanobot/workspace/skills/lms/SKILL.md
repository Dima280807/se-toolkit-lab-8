---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to answer questions about labs, learners, scores, and course progress.

## Available Tools

- `lms_health` — Check if the LMS backend is healthy and report the item count.
- `lms_labs` — List all labs available in the LMS.
- `lms_learners` — List all learners registered in the LMS.
- `lms_pass_rates` — Get pass rates (avg score and attempt count per task) for a lab.
- `lms_timeline` — Get submission timeline (date + submission count) for a lab.
- `lms_groups` — Get group performance (avg score + student count per group) for a lab.
- `lms_top_learners` — Get top learners by average score for a lab.
- `lms_completion_rate` — Get completion rate (passed / total) for a lab.
- `lms_sync_pipeline` — Trigger the LMS sync pipeline. May take a moment.

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. Call `lms_labs` first to get the list of available labs.
2. If multiple labs exist, use `mcp_webchat_ui_message` with `type: "choice"` to let the user pick a lab.
3. Provide short, readable labels using each lab's title field.
4. Use the lab's identifier (e.g., `lab-01`) as the stable value for the follow-up tool call.

### When the user names a specific lab:

- Call the appropriate tool directly with the lab parameter.
- Format numeric results nicely:
  - Percentages as `85%` not `0.85`
  - Counts as whole numbers
  - Scores with one decimal place if needed

### When the user asks "what can you do?":

- Explain that you can query the LMS backend for:
  - Lab availability and health status
  - Pass rates and scores per lab
  - Top learners and group performance
  - Submission timelines and completion rates
- Mention that you need a lab name for most detailed queries.

### Response Style

- Keep responses concise — summarize key findings, don't dump raw JSON.
- Use bullet points for multiple data points.
- When presenting lab choices, use the lab title as the user-facing label.
- Let the shared `structured-ui` skill decide how to present choices on supported channels.

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs`, then present a choice of labs using `mcp_webchat_ui_message`.

**User:** "How is the backend doing?"
**You:** Call `lms_health` and report: status, item count, any errors.

**User:** "Which lab has the lowest pass rate?"
**You:** Call `lms_labs`, then call `lms_pass_rates` for each lab, compare results, and report the lowest.

**User:** "Show me lab-04 scores"
**You:** Call `lms_pass_rates` with `lab: "lab-04"` and format the results.
