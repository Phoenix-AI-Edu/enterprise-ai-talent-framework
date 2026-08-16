<!-- OBSIDIAN-GOVERNANCE:BEGIN -->
## Obsidian central governance entry (managed block; do not edit manually)

- system_id: `SYS-03`
- repository: `AI_Talent`
- governance_center: `C:\Users\m1016\Documents\Obsidian`
- project_index: `10_Projects/Project-AI-Talent.md`
- sync_contract: `99_MOC/Repo-Governance-Sync.md`
- sync_manifest: `.obsidian-governance.json`

Before starting any work, read these canonical files in the Obsidian governance center:

1. `AGENTS.md`
2. `99_MOC/README.md`
3. `99_MOC/Governance-Rules.md`
4. `99_MOC/System-MOC.md`
5. `99_MOC/System-Registry.md`
6. `99_MOC/Repo-Governance-Sync.md`
7. `10_Projects/Project-AI-Talent.md`

Bidirectional synchronization rules:

1. Product, architecture, data-boundary, deployment, or commercial decisions: update Obsidian first, then this repo.
2. Code, schema, test, deployment, release, or incident changes: update this repo's repo-local records (see System-Registry.md), then write back to Obsidian `00_Inbox/CHANGELOG.md` and the related Project/Status files.
3. If either side is not synchronized, status must be `sync_pending`; do not mark the work complete.
4. If canonical governance conflicts with an old repo document, stop and follow the central precedence order. Code or an old `accepted` record cannot silently change product direction.
5. Before delivery, run Obsidian `scripts/Sync-Repo-Governance.ps1 -Mode Audit`. A failed audit blocks completion.

This block is managed by the central sync script. Repository-specific rules remain outside the markers.
<!-- OBSIDIAN-GOVERNANCE:END -->

# Repository-specific collaboration rules

Follow the central governance block above, then read this repository's README and task-specific instructions.
