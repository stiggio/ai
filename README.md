# Stigg AI

A collection of AI tools — skills, MCP servers, and agents — for working with [Stigg](https://stigg.io).

## What's Included

### Skills

| Skill                                                                | Description                                                                                     |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **[Product Catalog Management](skills/product-catalog-management/)** | Manage Stigg product catalogs via GraphQL API — export, merge, compare, and create environments |
| **[Stigg Docs](skills/stigg-docs/)**                                 | Reference documentation for the Stigg platform and APIs                                         |

> MCP servers and agents coming soon.

## Repo Structure

```
skills/
  product-catalog-management/   # Catalog operations (export, merge, environments)
  stigg-docs/                   # Platform & API reference docs
```

## Getting Started

Add the marketplace and install the plugin:

```bash
/plugin marketplace add stiggio/ai
/plugin install stigg@stigg
```

Once installed, skills are available as `/stigg:<skill-name>` and are also auto-invoked when Claude detects relevant context (e.g. mentions of "stigg", "product catalog", "pricing").

Each skill lives in its own directory under `skills/` with a `SKILL.md` that describes its capabilities, triggers, and usage.
