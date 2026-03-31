# Project Guidelines

This document describes the default project guidelines used by the DevMate assistant.

## General Rules
- Follow project guidelines before generating code.
- Prefer clear folder structure and readable module boundaries.
- Use `pyproject.toml` instead of `requirements.txt`.
- Use Python 3.13 and `uv` for dependency management.

## Backend Defaults
- For web APIs, prefer FastAPI.
- Add a `/health` endpoint.
- Use environment-aware configuration.

## Internal Notes
- When building a new coding project, consult project guidelines first.
- If a user asks for a new service, the assistant should check both network search and local project guidelines.