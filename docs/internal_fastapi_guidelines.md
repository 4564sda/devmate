# Internal FastAPI Guidelines

## Project Guidelines

This document defines the internal project guidelines for backend services built with FastAPI.

## API Design Rules

- Use **FastAPI** as the primary web framework.
- Organize routes by domain, for example:
  - `users`
  - `projects`
  - `tasks`
- All APIs should use clear REST-style naming.
- Return consistent JSON responses.

## Code Structure

Recommended project structure:

- `app/main.py` for FastAPI app entry
- `app/api/` for route definitions
- `app/services/` for business logic
- `app/models/` for data models
- `app/schemas/` for request and response schemas

## Validation Rules

- Use **Pydantic** models for request validation.
- Do not trust raw user input directly.
- Define explicit request and response schemas.

## Logging Rules

- Use the `logging` module.
- Do not use `print()`.
- Log important events such as:
  - application startup
  - request failures
  - external API errors

## Error Handling

- Use proper HTTP status codes.
- Provide readable error messages.
- Handle expected exceptions explicitly.

## Configuration Rules

- Store configuration in `config.toml`.
- Do not hardcode:
  - model names
  - API keys
  - base URLs
- Keep environment-specific secrets out of version control.

## Development Rules

- Follow PEP 8.
- Write modular code.
- Keep agent logic, tools, and retrieval logic separated.
- Prefer clear function names and type hints.

## RAG Notes

The local knowledge base may contain markdown files like this one.
The retrieval tool `search_knowledge_base(query)` should be able to find this file when the query includes:

- `project guidelines`
- `fastapi guidelines`
- `internal backend rules`

## Summary

Key project guidelines:

1. Use FastAPI.
2. Follow PEP 8.
3. Use logging instead of print.
4. Store configuration in `config.toml`.
5. Keep code modular and maintainable.