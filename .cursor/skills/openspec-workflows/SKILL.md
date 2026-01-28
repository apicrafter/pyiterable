---
name: openspec-workflows
description: OpenSpec proposal creation, validation, and implementation workflows. Use when creating change proposals, implementing specs, or working with OpenSpec conventions.
---

# OpenSpec Workflows

## When to Create Proposals

Create proposals for:
- New features or capabilities
- Breaking changes (API, schema)
- Architecture changes
- Performance optimizations (behavior changes)
- Security pattern updates

Skip proposals for:
- Bug fixes (restoring intended behavior)
- Typos, formatting, comments
- Non-breaking dependency updates
- Configuration changes
- Tests for existing behavior

## Quick Commands

```bash
openspec list                  # List active changes
openspec list --specs          # List specifications
openspec show [item]           # Display change or spec
openspec validate [item] --strict  # Validate changes
openspec archive <change-id> --yes  # Archive after deployment
```

## Creating Change Proposals

### 1. Context Checklist

Before starting:
- [ ] Read `openspec/project.md` for conventions
- [ ] Run `openspec list` to see active changes
- [ ] Run `openspec list --specs` to see existing capabilities
- [ ] Check for conflicts with pending changes

### 2. Choose Change ID

- Use kebab-case, verb-led: `add-`, `update-`, `remove-`, `refactor-`
- Examples: `add-two-factor-auth`, `update-parquet-support`
- Ensure uniqueness

### 3. Scaffold Structure

```bash
mkdir -p openspec/changes/<change-id>/specs/<capability>
```

Create:
- `proposal.md` - Why, what, impact
- `tasks.md` - Implementation checklist
- `design.md` - Only if needed (cross-cutting, architectural, or complex decisions)
- `specs/<capability>/spec.md` - Delta changes

### 4. Write Spec Deltas

Use operation headers:
- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior (include full requirement)
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

**Critical**: Every requirement MUST have at least one scenario:
```markdown
#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result
```

### 5. Validate

```bash
openspec validate <change-id> --strict
```

Fix all issues before sharing the proposal.

## Implementation Workflow

1. Read `proposal.md` - Understand what's being built
2. Read `design.md` (if exists) - Review technical decisions
3. Read `tasks.md` - Get implementation checklist
4. Implement tasks sequentially
5. Update checklist: mark all tasks `- [x]` when complete
6. **Do not start implementation until proposal is approved**

## Archiving Changes

After deployment:
```bash
openspec archive <change-id> --yes
```

This moves `changes/[name]/` → `changes/archive/YYYY-MM-DD-[name]/`

## Common Patterns

### Multi-Capability Changes

Create separate delta files:
```
changes/add-feature/
└── specs/
    ├── capability-a/
    │   └── spec.md   # ADDED: Feature A
    └── capability-b/
        └── spec.md   # ADDED: Feature B
```

### MODIFIED Requirements

Always include the complete requirement:
1. Copy entire requirement from `openspec/specs/<capability>/spec.md`
2. Paste under `## MODIFIED Requirements`
3. Edit to reflect new behavior
4. Keep at least one scenario

## Troubleshooting

**"Change must have at least one delta"**
- Check `changes/[name]/specs/` exists with .md files
- Verify files have operation prefixes

**"Requirement must have at least one scenario"**
- Use `#### Scenario:` format (4 hashtags)
- Don't use bullet points for scenario headers

**Debug delta parsing:**
```bash
openspec show [change] --json --deltas-only
```
