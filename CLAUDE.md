## Before You Start

`docs/agents/` contains notes from past sessions that may be relevant to your task. Consult when you need context; update when you learn something non-obvious.

## When You...

- **Learn something non-obvious** → Add a "When You..." entry here (keep this file under 100 lines), or update `docs/agents/`.

## Agent Notes

`docs/agents/` is the shared knowledge base for all LLM agents. Version-controlled and team-visible. Keep notes accurate, concise, and actionable.

## Skills & Tools

- `make format` — Format Python (docformatter, ruff, add-trailing-comma)
- `make lint` — Lint Python (ruff check, flake8/wemake)
- `make test` — Run tests with coverage (90% minimum)
- `make sync` — Sync config files via nitpick
- `make configure` — Check config files against nitpick spec
- `make check-py` — Run type checks via ty

## Quick Reference

- **Package**: `django_amp_renderer` — Django middleware for AMP server-side rendering
- **Dependencies**: `amp-renderer>=2.1`, `Django>=2.2`
- **Python**: 3.10+
- **CI**: GitHub Actions (lint on 3.13, test on 3.10–3.14)
