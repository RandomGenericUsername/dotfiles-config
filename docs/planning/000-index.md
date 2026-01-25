# Planning Documentation Index

> **Last Updated**: 2026-01-24

This directory contains all planning and specification documents for the dotfiles-config refactoring project.

---

## Document Overview

```
docs/planning/
├── 000-index.md                           # This file
├── 001-refactoring-knowledge-base.md      # Discovery & Analysis
├── 002-technical-requirements.md          # TRD - Requirements
├── 003-architecture-decision-records.md   # ADRs - Decisions
├── 004-feature-specifications.md          # Feature Specs
├── 005-implementation-tasks.md            # Tasks & Tickets
└── 006-test-plan.md                       # Test Strategy
```

---

## Document Relationships

```
┌─────────────────────────────────────────────────────────────┐
│           001-refactoring-knowledge-base.md                 │
│              (Discovery & Analysis Output)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┬─────────────────┐
          │               │               │                 │
          ▼               ▼               ▼                 ▼
┌─────────────────┐ ┌───────────┐ ┌───────────────┐ ┌─────────────┐
│ 002-technical-  │ │ 003-ADRs  │ │ 004-feature-  │ │ 006-test-   │
│ requirements.md │ │           │ │ specs.md      │ │ plan.md     │
│                 │ │           │ │               │ │             │
│ "SHALL" reqs    │ │ Decisions │ │ Behavior      │ │ Verification│
└────────┬────────┘ └───────────┘ └───────┬───────┘ └──────┬──────┘
         │                                │                │
         │          ┌─────────────────────┘                │
         │          │                                      │
         ▼          ▼                                      │
┌─────────────────────────────────────────┐               │
│       005-implementation-tasks.md       │◄──────────────┘
│              (Work Breakdown)           │
└─────────────────────────────────────────┘
```

---

## Documents Summary

### [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)
**Type**: Discovery & Analysis Output  
**Purpose**: Raw knowledge capture from analysis phase

Contains:
- Project context and goals
- Source code analysis
- Target architecture
- Module inventory with all features
- Architectural decisions (informal)
- API surface design
- Test strategy outline
- Implementation phases

### [002-technical-requirements.md](002-technical-requirements.md)
**Type**: Technical Requirements Document (TRD)  
**Purpose**: Formal "SHALL" requirements

Contains:
- General system requirements
- Project structure requirements
- Per-module functional requirements
- Error handling requirements
- CLI interface requirements
- API requirements
- Non-functional requirements
- Traceability matrix

### [003-architecture-decision-records.md](003-architecture-decision-records.md)
**Type**: Architecture Decision Records (ADRs)  
**Purpose**: Document and justify key decisions

Contains:
- ADR-001: Build Backend Selection (uv_build)
- ADR-002: Flat Project Hierarchy
- ADR-003: Dual Interface Pattern
- ADR-004: Naming Convention
- ADR-005: Fresh Test Suites
- ADR-006: Layered Architecture

### [004-feature-specifications.md](004-feature-specifications.md)
**Type**: Feature Specifications  
**Purpose**: Detailed behavior per feature

Contains:
- Packages module features (FS-PKG-*)
- Wallpapers module features (FS-WP-*)
- Icon Templates module features (FS-ICON-*)
- Root wrapper features (FS-ROOT-*)
- User stories, acceptance criteria, examples

### [005-implementation-tasks.md](005-implementation-tasks.md)
**Type**: Implementation Tasks / Tickets  
**Purpose**: Actionable work breakdown

Contains:
- Phase 1: Project Scaffolding (6 tasks)
- Phase 2: Packages Module (7 tasks)
- Phase 3: Wallpapers Module (6 tasks)
- Phase 4: Icon Templates Module (7 tasks)
- Phase 5: Root Wrapper Integration (4 tasks)
- Task dependencies and estimates

### [006-test-plan.md](006-test-plan.md)
**Type**: Test Plan  
**Purpose**: Test strategy and test cases

Contains:
- Test environment setup
- Shared fixtures
- Unit test cases per module
- Integration test cases per module
- Coverage requirements
- Requirements traceability matrix

---

## Quick Reference

### Requirements by Module

| Module | Requirements | Features | Tasks | Tests |
|--------|-------------|----------|-------|-------|
| General | REQ-GEN-* | - | Phase 1 | - |
| Packages | REQ-PKG-* | FS-PKG-* | Phase 2 | TC-PKG-* |
| Wallpapers | REQ-WP-* | FS-WP-* | Phase 3 | TC-WP-* |
| Icon Templates | REQ-ICON-* | FS-ICON-* | Phase 4 | TC-ICON-* |
| Root | REQ-ROOT-* | FS-ROOT-* | Phase 5 | TC-ROOT-* |

### Key Decisions

| Decision | Choice |
|----------|--------|
| Build Backend | `uv_build` |
| Project Hierarchy | Flat (top-level peers) |
| Interface Pattern | Dual (CLI + Python API) |
| Naming | `dotfiles-` prefix |
| Tests | Fresh start |
| Architecture | Three-layer (CLI → API → Service) |

### Estimated Effort

| Phase | Tasks | Hours |
|-------|-------|-------|
| Scaffolding | 6 | 2-3 |
| Packages | 7 | 4-6 |
| Wallpapers | 6 | 4-6 |
| Icon Templates | 7 | 6-8 |
| Root Wrapper | 4 | 2-3 |
| **Total** | **30** | **18-26** |

---

## Using These Documents

### For Implementation
1. Start with [005-implementation-tasks.md](005-implementation-tasks.md)
2. Reference [002-technical-requirements.md](002-technical-requirements.md) for requirements
3. Reference [004-feature-specifications.md](004-feature-specifications.md) for behavior details
4. Use [006-test-plan.md](006-test-plan.md) for test implementation

### For Understanding Decisions
- Read [003-architecture-decision-records.md](003-architecture-decision-records.md)

### For Full Context
- Start with [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

---

## Document History

| Date | Changes |
|------|---------|
| 2026-01-24 | Initial creation of all planning documents |
