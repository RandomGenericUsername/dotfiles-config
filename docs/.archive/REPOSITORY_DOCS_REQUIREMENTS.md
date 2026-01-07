# Repository Documentation Requirements Specification

> **Purpose**: This document provides complete requirements for an AI agent to generate comprehensive documentation for the entire dotfiles configuration system repository.

---

## Critical Guidelines: Zero Hallucination Policy

### Absolute Rules

1. **NEVER assume, ALWAYS verify**
   - Do NOT document features, commands, or behaviors not directly observable in source code or test execution
   - If a file/directory does not exist in the filesystem, do NOT document it
   - If a command does not appear in CLI help output, do NOT document it
   - If a test does not exist or pass, do NOT claim functionality works

2. **Source of Truth Hierarchy** (in order of priority)
   - **Primary**: Actual file contents (via Read tool)
   - **Secondary**: Command execution output (via Bash tool)
   - **Tertiary**: Passing test results (via pytest execution)
   - **INVALID**: Assumptions, inferences, "typical patterns", or "best practices" not evidenced in code

3. **Verification Requirements**
   - Before documenting any CLI command: RUN `config <command> --help` and use exact output
   - Before documenting any function: READ its source code
   - Before documenting any behavior: Either READ the implementation OR RUN the tests that verify it
   - Before documenting any configuration: READ the actual config file
   - Before documenting any API: READ the function signatures and docstrings

4. **When Information is Missing**
   - If a section cannot be documented due to missing source: Write `<!-- TODO: Source not available -->`
   - Do NOT invent examples that haven't been tested
   - Do NOT use hedging language like "typically", "usually", "should", "might"
   - If uncertain, mark with `[UNVERIFIED]` and explain what's missing

5. **Testing Requirements**
   - Run `make test` or `uv run pytest` before documenting functionality
   - Only document features that have passing tests OR can be verified via manual execution
   - Include test coverage information where available
   - Reference test files that verify documented behavior

### Mandatory Verification Commands

Execute these commands BEFORE writing any documentation:

```bash
# 1. Project Structure
tree -L 3 -I '.git|__pycache__|*.pyc|.pytest_cache|.venv'

# 2. CLI Interface
uv run config --help
uv run config install-packages --help
uv run config assets --help
uv run config assets wallpapers --help
uv run config assets wallpapers add --help
uv run config assets wallpapers list --help
uv run config assets wallpapers extract --help

# 3. Python Package Info
cat pyproject.toml
cat Makefile

# 4. Source Code Discovery
find src -name "*.py" -type f
find tests -name "*.py" -type f

# 5. Test Execution
uv run pytest -v --collect-only  # List all tests without running
uv run pytest -v                # Run all tests
uv run pytest -v --cov=src --cov-report=term-missing  # With coverage

# 6. Assets Discovery
find assets -type f
find config-files -type f

# 7. Ansible Package
cd packages/ansible && ansible-playbook --list-tags -i inventory/localhost.yml playbooks/bootstrap.yml
cd packages/ansible && ansible-playbook --list-tasks -i inventory/localhost.yml playbooks/bootstrap.yml
```

### Documentation Honesty Markers

Use these markers throughout documentation:

- `[VERIFIED via CLI]` - Verified by running the CLI command
- `[VERIFIED via tests]` - Verified by passing test suite
- `[VERIFIED via source]` - Verified by reading source code
- `[PLACEHOLDER]` - Exists in structure but not yet implemented
- `[UNTESTED]` - Code exists but no tests verify behavior
- `[DEPRECATED]` - Marked as deprecated in source

---

## Repository Overview

### What This Project Is

A **Python-based CLI tool** for managing dotfiles configuration:
- Contains configuration files (not an installer itself)
- Provides CLI commands to access/manage configs
- Integrates with external installer via CLI interface
- Built with Python 3.12+, Typer framework, and Ansible

### Project Components

| Component | Location | Purpose | Must Verify |
|-----------|----------|---------|-------------|
| CLI Application | `src/` | Main Python application code | Read all `.py` files |
| Commands | `src/commands/` | CLI command implementations | Run `--help` for each |
| Tests | `tests/` | Unit and integration tests | Run test suite |
| Config Files | `config-files/` | Actual configuration files (nvim, zsh, etc.) | List files |
| Assets | `assets/` | Icons, wallpapers, etc. | List files |
| Ansible Package | `packages/ansible/` | Package installation system | See DOCS_REQUIREMENTS.md |
| Build System | `Makefile`, `pyproject.toml` | Development tooling | Read files |

---

## Documentation Structure

Create the following directory structure under repository root:

```
docs/
├── index.md                    # Main documentation entry point
│
├── getting-started/
│   ├── index.md                # Quick start
│   ├── installation.md         # Development setup
│   ├── first-steps.md          # First commands to try
│   └── project-structure.md    # Understanding the layout
│
├── architecture/
│   ├── index.md                # Architecture overview
│   ├── design-principles.md    # Why things are structured this way
│   ├── cli-structure.md        # Command hierarchy and organization
│   ├── directory-layout.md     # Detailed directory explanations
│   └── integration-points.md   # How external installer integrates
│
├── reference/
│   ├── index.md                # Reference overview
│   │
│   ├── cli/
│   │   ├── index.md            # CLI reference overview
│   │   ├── install-packages.md # install-packages command
│   │   ├── assets/
│   │   │   ├── index.md        # assets group
│   │   │   └── wallpapers.md   # wallpapers subcommand
│   │   └── dummy.md            # dummy command
│   │
│   ├── python-api/
│   │   ├── index.md            # Python API overview
│   │   ├── commands.md         # Command modules
│   │   └── services.md         # Service modules
│   │
│   ├── config-files/
│   │   ├── index.md            # Config files overview
│   │   ├── nvim.md             # Neovim configuration
│   │   └── zsh.md              # Zsh configuration
│   │
│   └── assets/
│       ├── index.md            # Assets overview
│       ├── wallpapers.md       # Wallpaper assets
│       ├── icons.md            # Icon sets
│       └── file-formats.md     # Asset file formats/structure
│
├── guides/
│   ├── index.md                # Guides overview
│   ├── development/
│   │   ├── index.md            # Development guides overview
│   │   ├── setup.md            # Setting up dev environment
│   │   ├── running-tests.md    # How to run tests
│   │   ├── adding-commands.md  # Adding new CLI commands
│   │   └── code-style.md       # Coding standards
│   │
│   ├── usage/
│   │   ├── index.md            # Usage guides overview
│   │   ├── managing-wallpapers.md  # Wallpaper management
│   │   ├── installing-packages.md  # Package installation
│   │   └── custom-configs.md       # Customizing configs
│   │
│   └── integration/
│       ├── index.md            # Integration guides overview
│       ├── installer-integration.md  # How installer uses this
│       └── ci-cd.md            # CI/CD integration
│
├── examples/
│   ├── index.md                # Examples overview
│   ├── cli-usage.md            # CLI usage examples
│   ├── wallpaper-workflow.md   # Complete wallpaper workflow
│   └── package-installation.md # Package installation examples
│
└── testing/
    ├── index.md                # Testing overview
    ├── running-tests.md        # How to run the test suite
    ├── test-structure.md       # Test organization
    ├── writing-tests.md        # How to write new tests
    └── coverage.md             # Test coverage info
```

---

## Root README.md Requirements

### Purpose
Top-level entry point for the entire repository.

### Must Include (VERIFIED content only)

1. **Project Title and Badges**
   - Project name (from `pyproject.toml`)
   - Python version badge (from `requires-python` in pyproject.toml)
   - Test status (if CI exists, otherwise omit)

2. **One-Line Description**
   - Extract from `pyproject.toml` description field
   - If empty, write: `<!-- TODO: Add description to pyproject.toml -->`

3. **Features** (only those verifiable)
   - List ONLY commands that appear in `config --help`
   - Reference asset types that exist in `assets/` directory
   - Reference config files that exist in `config-files/` directory

4. **Quick Start**
   - Installation steps (from Makefile targets)
   - One example command that actually works

5. **Documentation Link**
   - Link to `docs/index.md`

6. **Project Structure** (high-level)
   - Generated from actual `tree` output
   - Include brief description of each top-level directory

7. **Requirements**
   - From `pyproject.toml` `requires-python`
   - From `pyproject.toml` `dependencies`

8. **Development**
   - Link to development guide
   - Quick commands from Makefile

### Must NOT Include
- Feature descriptions for unimplemented commands
- Aspirational roadmap items
- Assumed behaviors not in code

---

## Content Requirements Per Documentation File

### `docs/index.md`

**Purpose**: Main documentation landing page

**Verification Required**:
- Run `tree` to verify project structure
- Run `config --help` to verify CLI commands
- Read `pyproject.toml` for project metadata

**Must Include**:
- Welcome and project purpose
- Documentation navigation (table of contents)
- Quick links to most common tasks
- How documentation is organized

---

### Getting Started Section

#### `docs/getting-started/installation.md`

**Verification Required**:
- Read `Makefile` for available targets
- Run `make help` to verify targets
- Read `pyproject.toml` for dependencies

**Must Include**:
- Prerequisites (Python version from pyproject.toml)
- Installation steps (using Makefile targets)
- Verification steps (run CLI to confirm)
- Troubleshooting common issues (ONLY if documented or observed)

#### `docs/getting-started/first-steps.md`

**Verification Required**:
- Run each suggested command to verify it works
- Capture actual output

**Must Include**:
- `config --help` output and explanation
- One working example per command group
- Expected output for each example

#### `docs/getting-started/project-structure.md`

**Verification Required**:
- Run `tree` command for actual structure
- Read each component to understand purpose

**Must Include**:
- Directory tree (from `tree` output)
- Purpose of each directory (derived from contents)
- Key files and their roles
- Where to find what you need

---

### Architecture Section

#### `docs/architecture/cli-structure.md`

**Verification Required**:
- Run `config --help` and all subcommand `--help`
- Read `src/main.py` to understand registration
- Read command files to understand hierarchy

**Must Include**:
- Command hierarchy diagram (from actual `--help` output)
- How commands are registered (from `main.py`)
- Command group organization (from source code structure)
- Parameter passing and context handling

#### `docs/architecture/directory-layout.md`

**Verification Required**:
- Run `find` or `tree` for actual layout
- Read files to understand conventions

**Must Include**:
- Complete directory structure
- Purpose of each directory (evidence-based)
- File naming conventions (observed patterns)
- Import structure and dependencies

#### `docs/architecture/integration-points.md`

**Verification Required**:
- Read `install_packages.py` to see how ansible is called
- Read `pyproject.toml` `[project.scripts]` for entry point
- Examine how variables can be passed

**Must Include**:
- How external installer calls this CLI
- Environment variables used (if any)
- Exit codes and error handling
- Data flow between components

---

### Reference Section

#### `docs/reference/cli/*.md` (One file per command)

**Verification Required**:
- Run `config <command> --help` for EXACT output
- Read command source file
- Run command with various arguments to verify behavior
- Check if tests exist for the command

**Must Include for EACH command**:
1. **Command Synopsis**
   ```bash
   config <command> [OPTIONS] [ARGS]
   ```

2. **Description**
   - What the command does (from source code or help text)

3. **Options** (from `--help` output)
   | Option | Type | Default | Description |
   |--------|------|---------|-------------|
   | Exact options from --help output |

4. **Arguments** (from `--help` output)
   | Argument | Required | Description |
   |----------|----------|-------------|

5. **Examples** (TESTED examples only)
   - Each example must be runnable
   - Include expected output
   - Mark with `[VERIFIED]`

6. **Exit Codes**
   - 0 = success (standard)
   - Other codes (ONLY if explicitly handled in source)

7. **Related Commands**
   - Links to related commands

8. **Source Reference**
   - Link to source file: `src/commands/<file>.py`
   - Link to test file (if exists): `tests/*/test_<name>.py`

#### `docs/reference/python-api/*.md`

**Verification Required**:
- Read ALL source files in `src/`
- Extract docstrings
- Examine function signatures
- Verify imports and dependencies

**Must Include**:
- Module purpose and overview
- Public API functions/classes (from `__init__.py` exports or source)
- Function signatures (exact from source)
- Parameters and return types (from type hints if present)
- Docstrings (verbatim from source)
- Usage examples (from tests if available)

**Format for Each Function/Class**:
```markdown
### `function_name(param1: type, param2: type) -> return_type`

[Docstring from source]

**Parameters:**
- `param1` (type): Description [from docstring or code]
- `param2` (type): Description

**Returns:**
- return_type: Description

**Raises:**
- ExceptionType: When [from code inspection]

**Example:**
```python
# Example from tests or verified manual test
```

**Source:** `src/path/to/file.py:line_number`
**Tests:** `tests/path/to/test.py:line_number` [if exists]
```

#### `docs/reference/config-files/*.md`

**Verification Required**:
- List all files in `config-files/<name>/`
- Read configuration files
- Understand what each config does (from comments or structure)

**Must Include**:
- Purpose of the configuration
- Files included (from directory listing)
- Key configuration sections (from reading the config)
- How this config is used (from ansible roles or documentation)
- Installation location (from ansible role or code)

#### `docs/reference/assets/*.md`

**Verification Required**:
- List all files in `assets/<category>/`
- Examine file formats
- Read any asset README files
- Check how assets are managed (read wallpapers service code)

**Must Include**:
- Asset category overview
- File structure (from directory listing)
- File formats used (from file inspection)
- How to add new assets (from service code or existing README)
- How assets are accessed (from service code)

---

### Guides Section

#### `docs/guides/development/adding-commands.md`

**Verification Required**:
- Read existing command files to extract patterns
- Read `main.py` registration code
- Examine test files for command testing patterns

**Must Include**:
1. **Step-by-step process** (derived from existing code structure)
   - Create command file in `src/commands/`
   - Implement command function
   - Register in `main.py`
   - Add tests
   - Update documentation

2. **Code templates** (extracted from existing commands)
   - Minimal command template (from dummy.py or similar)
   - Command with options template (from real example)
   - Command group template (from assets/__init__.py)

3. **Testing requirements** (from existing test structure)
   - Where to put tests
   - Test naming conventions (observed)
   - Example test (from existing tests)

4. **Documentation requirements**
   - What docs to update

**CRITICAL**: All templates must be derived from actual working code in the repository.

#### `docs/guides/development/running-tests.md`

**Verification Required**:
- Read `Makefile` test targets
- Run `make test`, `make test-unit`, `make test-integration`
- Run `uv run pytest --help` to see pytest options
- Read `pyproject.toml` pytest configuration

**Must Include**:
- Test command options (from Makefile)
- How to run specific tests (verified pytest syntax)
- How to run with coverage (from Makefile)
- How to run in verbose mode
- Interpreting test output (from actual output)

#### `docs/guides/usage/managing-wallpapers.md`

**Verification Required**:
- Run all `config assets wallpapers` subcommands
- Read `wallpapers/service.py` to understand functionality
- Read tests for wallpapers to see usage patterns
- Test actual wallpaper operations

**Must Include**:
- Complete workflow with real commands
- Adding wallpapers (tested command)
- Listing wallpapers (tested command)
- Extracting wallpapers (tested command)
- File format requirements (from service code)
- Error cases and handling (from source or tests)

---

### Examples Section

#### `docs/examples/cli-usage.md`

**Verification Required**:
- Run EVERY example command before documenting
- Capture actual output
- Verify exit codes

**Must Include**:
- Real, tested examples for each command
- Expected output for each example
- Explanation of what's happening
- Common variations

**Format**:
```markdown
### Example: [Description]

[VERIFIED via CLI - 2026-01-03]

```bash
$ config command --option value
[actual output]
```

**Explanation:**
[what the command does]

**Expected outcome:**
[what should happen]
```

---

### Testing Section

#### `docs/testing/test-structure.md`

**Verification Required**:
- List all test files
- Read `conftest.py` for fixtures
- Examine test organization
- Read `pyproject.toml` pytest config

**Must Include**:
- Directory structure (from `tree tests/`)
- Unit vs integration split (observed structure)
- Fixtures available (from conftest.py)
- Naming conventions (observed patterns)
- How tests are discovered (from pytest config)

#### `docs/testing/coverage.md`

**Verification Required**:
- Run `make test-cov` or equivalent
- Capture coverage report
- Identify untested areas

**Must Include**:
- Current coverage percentage (from report)
- Coverage by module (from report)
- Uncovered lines (from report)
- How to generate coverage report

---

## Style Guidelines

### General Principles
- Use GitHub-flavored Markdown
- Clear, concise, technical writing
- Present tense, active voice
- Second person ("you") for instructions
- No emojis or excessive formatting
- No marketing language or superlatives

### Code Examples
- All code examples must be tested
- Include `[VERIFIED]` marker with date
- Use proper syntax highlighting
- Show actual output, not "..."
- Include error cases where relevant

### Headings
- One `#` title per file
- Sentence case
- Descriptive, not clever

### Links
- Use relative links between docs
- Link to source files with line numbers where helpful
- Use format: `[file.py:42](../src/file.py#L42)`

### Tables
- Use for structured reference data
- Keep readable (not too wide)
- Include units/types where relevant

### Verification Markers
Always include verification markers:
```markdown
[VERIFIED via CLI - 2026-01-03]
[VERIFIED via tests - 2026-01-03]
[VERIFIED via source - src/main.py:15]
```

---

## Forbidden Actions

**DO NOT**:

1. Document commands not in `--help` output
2. Document functions not in source code
3. Document tests that don't exist or fail
4. Create examples that haven't been tested
5. Assume behavior not evidenced in code
6. Use words like: typically, usually, should, might, probably, generally
7. Add TODOs for future features unless they're already in code comments
8. Document configuration options not in actual config files
9. Describe CLI options not in `--help` output
10. Reference external projects/tools without verifying integration exists
11. Claim test coverage without running tests
12. Invent error messages not in source code
13. Assume exit codes without checking source
14. Document environment variables not read in code
15. Describe file formats without examining actual files

---

## Source Files Manifest

Before writing ANY documentation, create a manifest of all source files:

### Python Source Files
```bash
find src -name "*.py" -type f | sort
```

### Test Files
```bash
find tests -name "*.py" -type f | sort
```

### Configuration Files
```bash
find config-files -type f | sort
```

### Asset Files
```bash
find assets -type f | sort
```

### Package Files
```bash
find packages -type f \( -name "*.yml" -o -name "*.yaml" -o -name "*.cfg" \) | sort
```

**Requirement**: Document ONLY files that appear in this manifest.

---

## Validation Checklist

Before submitting documentation:

### Structure Validation
- [ ] All files in documentation structure exist
- [ ] All internal links are valid (no 404s)
- [ ] All source file references are accurate
- [ ] Directory structure matches specification

### Content Validation
- [ ] Every CLI command documented exists in `--help` output
- [ ] Every function documented exists in source
- [ ] Every configuration option documented exists in config files
- [ ] Every example has been tested and output verified
- [ ] No hedging language (typically, usually, etc.)
- [ ] All verification markers present

### Technical Validation
```bash
# All CLI examples are valid
grep -r '```bash' docs/ | # extract commands | # run each

# All source references exist
grep -r 'src/.*\.py' docs/ | # extract paths | # verify each exists

# All test references exist
grep -r 'tests/.*\.py' docs/ | # extract paths | # verify each exists

# No placeholder text remains (except where source is genuinely missing)
grep -r 'TODO\|FIXME\|XXX' docs/ | grep -v '<!-- TODO: Source not available -->'
```

### Test Validation
- [ ] Run full test suite: `make test`
- [ ] All tests pass
- [ ] Coverage report generated: `make test-cov`
- [ ] Coverage percentage documented accurately

---

## Execution Order

### Phase 1: Discovery (No Writing)
1. Clone/checkout repository
2. Run ALL verification commands
3. Create source files manifest
4. Run complete test suite
5. Generate coverage report
6. Build internal knowledge map

### Phase 2: Reference Material (Facts Only)
1. Document `reference/cli/` (from `--help` outputs)
2. Document `reference/python-api/` (from source reading)
3. Document `reference/config-files/` (from file inspection)
4. Document `reference/assets/` (from directory inspection)
5. Document `testing/test-structure.md` (from test inspection)
6. Document `testing/coverage.md` (from coverage report)

### Phase 3: Architecture (Understanding)
1. Document `architecture/cli-structure.md`
2. Document `architecture/directory-layout.md`
3. Document `architecture/integration-points.md`
4. Document `architecture/design-principles.md`

### Phase 4: Getting Started (User Entry)
1. Document `getting-started/installation.md`
2. Document `getting-started/first-steps.md`
3. Document `getting-started/project-structure.md`

### Phase 5: Guides (Task-Oriented)
1. Document development guides
2. Document usage guides
3. Document integration guides

### Phase 6: Examples (Practical)
1. Create and test all examples
2. Document examples

### Phase 7: Top-Level (Navigation)
1. Write `docs/index.md`
2. Write root `README.md`
3. Update section index files

### Phase 8: Validation
1. Run all validation checklist items
2. Fix any issues found
3. Generate final documentation

---

## Special Considerations

### Ansible Package
- Already has specification in `packages/ansible/DOCS_REQUIREMENTS.md`
- Reference that specification
- Ensure consistency between repo docs and ansible docs
- Link from repo docs to ansible docs

### Testing Philosophy
- All functionality should have tests
- If no tests exist, mark as `[UNTESTED]`
- Prefer documenting tested behavior
- When documenting untested code, caveat clearly

### CLI Evolution
- CLI may change
- Documentation must stay synchronized
- Include verification dates on CLI examples
- Use `--help` output as source of truth

### External Dependencies
- Document only what's in `pyproject.toml` dependencies
- Don't document optional features unless implemented
- Reference official docs for external tools (don't duplicate)

---

## Output Format

All documentation should be:
- Plain Markdown (.md files)
- UTF-8 encoded
- Unix line endings (LF)
- No trailing whitespace
- Blank line at end of file
- Headings have blank line before and after
- Code blocks have blank line before and after

---

## Success Criteria

Documentation is complete when:

1. ✅ Every CLI command has reference docs
2. ✅ Every Python module has API docs
3. ✅ Every config file has explanation
4. ✅ Every asset type has description
5. ✅ Development setup is documented and tested
6. ✅ Test suite usage is documented
7. ✅ Integration points are explained
8. ✅ Examples work when copy-pasted
9. ✅ All verification markers present
10. ✅ All validation checks pass
11. ✅ Zero assumptions, only verified facts
12. ✅ User can onboard from docs alone

---

## Meta: About This Document

This document itself should be:
- Kept in repository root as `REPOSITORY_DOCS_REQUIREMENTS.md`
- Updated when new components are added
- Referenced by documentation contributors
- Version controlled alongside code
- Reviewed when documentation standards change
