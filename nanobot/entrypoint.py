#!/usr/bin/env python3
"""Resolve environment variables into config.json and launch nanobot gateway."""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    config_dir = Path(__file__).parent
    config_path = config_dir / "config.json"
    resolved_path = config_dir / "config.resolved.json"
    workspace_dir = config_dir / "workspace"

    # Read base config
    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base = os.environ.get("LLM_API_BASE_URL")
    llm_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base:
        config["providers"]["custom"]["apiBase"] = llm_api_base
    if llm_model:
        config["agents"]["defaults"]["model"] = llm_model

    # Resolve gateway settings
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Resolve MCP LMS server env vars
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if "lms" in config.get("tools", {}).get("mcpServers", {}):
        if lms_backend_url:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Resolve MCP webchat server env vars (if configured)
    webchat_relay_url = os.environ.get("NANOBOT_WEBCCHAT_RELAY_URL")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if "webchat" in config.get("tools", {}).get("mcpServers", {}):
        if webchat_relay_url:
            config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCCHAT_RELAY_URL"] = webchat_relay_url
        if access_key:
            config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_ACCESS_KEY"] = access_key

    # Resolve webchat channel settings
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")

    if webchat_host and "webchat" in config.get("channels", {}):
        config["channels"]["webchat"]["host"] = webchat_host
    if webchat_port and "webchat" in config.get("channels", {}):
        config["channels"]["webchat"]["port"] = int(webchat_port)

    # Enable webchat channel if env var is set
    if webchat_port and "webchat" not in config.get("channels", {}):
        config.setdefault("channels", {})["webchat"] = {
            "enabled": True,
            "host": webchat_host or "0.0.0.0",
            "port": int(webchat_port),
            "allowFrom": ["*"],
        }

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}", file=sys.stderr)

    # Launch nanobot gateway using the full path from the virtual environment
    # The venv is at /app/.venv (root level), not inside /app/nanobot
    venv_bin = "/app/.venv/bin"
    nanobot_path = os.path.join(venv_bin, "nanobot")
    
    os.execvp(
        nanobot_path,
        [
            nanobot_path,
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
