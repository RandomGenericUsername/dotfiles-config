# Documentation Requirements Specification

> **Purpose**: This document provides complete requirements for an AI agent to generate documentation for the ansible package within the dotfiles configuration system.

---

## Critical Guidelines: Zero Hallucination Policy

### Absolute Rules

1. **NEVER assume, ALWAYS verify**
   - Do NOT write documentation for features, variables, or behaviors that you have not directly observed in source files
   - If a file does not exist, do NOT document it
   - If a variable is not defined in source, do NOT document it

2. **Source of Truth Hierarchy**
   - Primary: Actual file contents (read via tools)
   - Secondary: Command output (run via shell)
   - INVALID: Assumptions, inferences, "common patterns", or "typical ansible behavior"

3. **Verification Requirements**
   - Before documenting any variable: READ the file where it's defined
   - Before documenting any role: READ all files in that role's directory
   - Before documenting any tag: GREP for the tag in playbook files
   - Before documenting any behavior: Either READ the task file OR RUN the playbook in check mode

4. **When Information is Missing**
   - If a section cannot be documented due to missing source information, write: `<!-- TODO: Source file not found or empty -->`
   - Do NOT invent content to fill gaps
   - Do NOT use phrases like "typically", "usually", "commonly" to mask uncertainty

5. **Testing Before Documenting**
   - Run `ansible-playbook --list-tasks` to verify task names
   - Run `ansible-playbook --list-tags` to verify available tags
   - Run `ansible-playbook --check` to verify behavior without making changes
   - Use `ansible-inventory --list` to verify inventory structure

### Verification Commands

Before writing documentation, execute these commands and use their output as source of truth:

```bash
# Verify directory structure
find packages/ansible -type f -name "*.yml" -o -name "*.yaml" -o -name "*.cfg"

# List all tags
ansible-playbook -i packages/ansible/inventory/localhost.yml packages/ansible/playbooks/bootstrap.yml --list-tags

# List all tasks
ansible-playbook -i packages/ansible/inventory/localhost.yml packages/ansible/playbooks/bootstrap.yml --list-tasks

# Verify inventory
ansible-inventory -i packages/ansible/inventory/localhost.yml --list

# Check playbook syntax
ansible-playbook -i packages/ansible/inventory/localhost.yml packages/ansible/playbooks/bootstrap.yml --syntax-check
```

### Documentation Honesty Markers

Use these markers in documentation when appropriate:

- `[VERIFIED]` - Content verified by reading source file or running command
- `[PLACEHOLDER]` - Directory/file exists but is empty, documented for structure
- `[UNTESTED]` - Documented from source but not execution-tested

---

## Project Context

### What This Project Is
- A **dotfiles configuration system** containing only configuration files (no installation logic)
- Designed to be used via CLI by an external installer project
- The installer calls CLI commands to execute ansible playbooks for package installation
- Uses variables that can be overridden by the installer (e.g., `dotfiles_root`)

### What This Ansible Package Does
- Installs and configures software packages on the local machine
- Copies configuration files from the dotfiles repository to their target locations
- Supports multiple Linux distributions (Debian, Fedora, Archlinux)
- Uses tags for selective role execution

---

## Source Files Reference

**MANDATORY**: Read ALL these files before writing any documentation. Do NOT proceed if any file cannot be read.

| File | Purpose | Action |
|------|---------|--------|
| `ansible.cfg` | Ansible configuration | READ and extract: inventory path, roles_path |
| `inventory/localhost.yml` | Host definition | READ and extract: connection type, python interpreter |
| `inventory/group_vars/all.yml` | Global variables | READ and extract: ALL variable definitions exactly as written |
| `playbooks/bootstrap.yml` | Main playbook | READ and extract: play name, roles, tags, pre_tasks |
| `playbooks/roles/base/` | Base roles directory | LIST contents, note if empty |
| `playbooks/roles/features/` | Feature roles directory | LIST all subdirectories |
| `playbooks/roles/features/nvim/tasks/main.yml` | Neovim tasks | READ and extract: ALL task names and modules used |
| `playbooks/roles/features/nvim/defaults/main.yml` | Neovim defaults | READ and extract: ALL variable definitions |
| `playbooks/roles/features/nvim/vars/main.yml` | Neovim vars | READ and extract: ALL variable definitions |

### File Reading Protocol

For each source file:
1. Attempt to read the file
2. If file exists and has content: Document exactly what is there
3. If file exists but is empty: Note as `[PLACEHOLDER]`
4. If file does not exist: Note as `[MISSING]` and do NOT invent content
5. If directory is empty: Note as `[EMPTY DIRECTORY]`

---

## Documentation Structure

Create the following directory structure under `packages/ansible/`:

```
packages/ansible/
├── README.md
└── docs/
    ├── index.md
    ├── getting-started/
    │   ├── index.md
    │   ├── prerequisites.md
    │   └── installation.md
    ├── architecture/
    │   ├── index.md
    │   ├── directory-structure.md
    │   ├── variable-system.md
    │   └── roles-organization.md
    ├── reference/
    │   ├── index.md
    │   ├── variables.md
    │   ├── tags.md
    │   ├── distributions.md
    │   └── roles/
    │       ├── index.md
    │       ├── base/
    │       │   └── index.md
    │       └── features/
    │           ├── index.md
    │           └── nvim.md
    ├── guides/
    │   ├── index.md
    │   ├── adding-a-role.md
    │   ├── adding-distribution-support.md
    │   └── integration.md
    └── examples/
        ├── index.md
        ├── basic-usage.md
        ├── custom-paths.md
        └── selective-install.md
```

---

## Content Requirements Per File

### `README.md`

**Purpose**: Entry point, minimal, directs users to docs

**Must Include**:
- Project title
- One-line description
- Quick example command (COPY from existing README.md or construct from verified source)
- Link to `docs/index.md`

**Must NOT Include**:
- Detailed explanations (those go in docs/)
- Full variable references
- Complete usage guides

**Verification**: Read existing README.md first, preserve any accurate existing content

---

### `docs/index.md`

**Purpose**: Documentation home page with navigation

**Must Include**:
- Welcome message and project overview (2-3 paragraphs)
- How this fits into the larger dotfiles system
- Quick navigation table/list to all sections
- Quick start snippet (use ONLY verified command structure)

---

### `docs/getting-started/index.md`

**Purpose**: Quick start guide

**Must Include**:
- Minimal steps to run the playbook
- Link to prerequisites and installation for details
- Basic command example (VERIFIED by checking ansible.cfg paths)

---

### `docs/getting-started/prerequisites.md`

**Purpose**: System requirements

**Must Include**:
- Required software: ansible (VERIFY version by running `ansible --version` if possible)
- Python interpreter path (EXTRACT from `inventory/localhost.yml`)
- Required permissions (EXTRACT from tasks that use `become: true`)

**Verification**: Run `ansible --version` to get actual version info

---

### `docs/getting-started/installation.md`

**Purpose**: Setup instructions

**Must Include**:
- How to install ansible (reference official docs, do NOT invent commands)
- How to verify the setup (use `ansible-playbook --syntax-check`)

---

### `docs/architecture/index.md`

**Purpose**: High-level architecture overview

**Must Include**:
- Component relationships (DERIVED from reading ansible.cfg and playbooks)
- Design philosophy (ONLY if documented in source, otherwise mark as inferred)
- How external installer interacts (based on variable override mechanism in group_vars)

---

### `docs/architecture/directory-structure.md`

**Purpose**: Detailed project layout explanation

**Must Include**:
- Full directory tree (GENERATE using `find` or `tree` command)
- Purpose of each directory (DERIVE from contents, not assumptions)
- Purpose of each configuration file (DERIVE from file contents)

**CRITICAL**: Run `tree` or `find` command to get actual structure. Do NOT assume structure.

---

### `docs/architecture/variable-system.md`

**Purpose**: Explain variable flow and override hierarchy

**Must Include**:
- Variable precedence (reference ansible documentation for standard precedence)
- Variables from `group_vars/all.yml` (COPY exactly from file)
- How role `defaults/` vs `vars/` work (reference ansible documentation)
- How external installer can override variables via `-e` flag

**Key Variables to Document** (EXTRACT directly from `group_vars/all.yml`):
- List ONLY variables that exist in the file
- Use EXACT variable names and default values from source

---

### `docs/architecture/roles-organization.md`

**Purpose**: Explain base vs features role categories

**Must Include**:
- What is in `base/` (LIST actual contents)
- What is in `features/` (LIST actual contents)
- Standard role directory structure (DERIVE from existing role structure)

**Verification**: `ls -la playbooks/roles/base/` and `ls -la playbooks/roles/features/`

---

### `docs/reference/index.md`

**Purpose**: Reference section overview

**Must Include**:
- What reference docs contain
- Navigation to all reference docs

---

### `docs/reference/variables.md`

**Purpose**: Complete variable reference

**Must Include**:
- Table of all global variables from `group_vars/all.yml` (EXTRACT exactly)
- Table of role-specific variables per role (EXTRACT from defaults/main.yml and vars/main.yml)

**Format**:
```markdown
| Variable | Default | Description | Source File |
|----------|---------|-------------|-------------|
| `variable_name` | `exact_default_value` | Description | `path/to/file.yml` |
```

**CRITICAL**: Every variable in this table MUST have a corresponding line in a source file.

---

### `docs/reference/tags.md`

**Purpose**: Document available tags

**Must Include**:
- Table of all available tags

**Verification**: Run `ansible-playbook --list-tags` and document ONLY tags that appear in output.

---

### `docs/reference/distributions.md`

**Purpose**: Document distribution support

**Must Include**:
- List of supported distributions (EXTRACT from vars/main.yml package maps)
- Package name mappings (EXTRACT exactly from source)

**CRITICAL**: Only list distributions that appear in package mapping variables.

---

### `docs/reference/roles/index.md`

**Purpose**: Roles overview

**Must Include**:
- List of all roles (GENERATE by listing directories in roles/)
- Links to detailed role docs

**Verification**: `find playbooks/roles -mindepth 2 -maxdepth 2 -type d`

---

### `docs/reference/roles/base/index.md`

**Purpose**: Base roles category overview

**Must Include**:
- List of roles in base/ (may be empty)
- Note if empty: "No base roles have been implemented yet."

---

### `docs/reference/roles/features/index.md`

**Purpose**: Features roles category overview

**Must Include**:
- List of all roles in features/ (from directory listing)
- Links to each role's documentation

---

### `docs/reference/roles/features/nvim.md`

**Purpose**: Neovim role documentation

**Must Include** (ALL extracted from source files):
- Tag name (from bootstrap.yml)
- Tasks performed (EXACT task names from tasks/main.yml)
- Variables (from defaults/main.yml with exact names and defaults)
- Package mappings (from vars/main.yml with exact distribution names and packages)

**Source Files to Read**:
- `playbooks/roles/features/nvim/tasks/main.yml`
- `playbooks/roles/features/nvim/defaults/main.yml`
- `playbooks/roles/features/nvim/vars/main.yml`

---

### `docs/guides/index.md`

**Purpose**: Guides section overview

**Must Include**:
- List of available guides with descriptions

---

### `docs/guides/adding-a-role.md`

**Purpose**: Step-by-step guide to create new roles

**Must Include**:
- Role directory structure (DERIVE from existing nvim role structure)
- Required files (based on what nvim role has)
- Template examples (based on nvim role file contents)

**CRITICAL**: Use nvim role as the template. Do NOT invent patterns that don't exist in the codebase.

---

### `docs/guides/adding-distribution-support.md`

**Purpose**: How to add support for new distributions

**Must Include**:
- How distribution detection works (reference `ansible_facts['distribution']`)
- Where to add package mappings (based on nvim role's vars/main.yml structure)

---

### `docs/guides/integration.md`

**Purpose**: How external installer integrates

**Must Include**:
- Command structure (DERIVE from ansible.cfg paths)
- Variable override mechanism (based on group_vars structure)

**Example command construction**:
```bash
# Construct from verified paths:
# - Inventory: from ansible.cfg [defaults] inventory
# - Playbook: from playbooks/ directory listing
ansible-playbook -i <inventory_path> <playbook_path> [options]
```

---

### `docs/examples/index.md`

**Purpose**: Examples section overview

---

### `docs/examples/basic-usage.md`

**Purpose**: Common usage patterns

**Must Include**:
- Commands constructed from verified paths only
- Tag examples using only verified tags

---

### `docs/examples/custom-paths.md`

**Purpose**: Overriding default paths

**Must Include**:
- Override examples using ONLY variables that exist in group_vars/all.yml

---

### `docs/examples/selective-install.md`

**Purpose**: Using tags for partial installs

**Must Include**:
- Tag examples using ONLY tags found via `--list-tags`

---

## Style Guidelines

### General
- Use GitHub-flavored Markdown
- Keep language clear and concise
- Use present tense
- Use second person ("you") for instructions
- No emojis

### Code Blocks
- Use fenced code blocks with language identifier
- Use `yaml` for ansible/YAML files
- Use `bash` for shell commands
- Use `text` for directory trees

### Links
- Use relative links between docs
- Link to source files where relevant

### Tables
- Use tables for reference data
- Include "Source File" column for traceability

---

## Validation Checklist

After generating documentation, verify:

- [ ] All files in the structure exist
- [ ] All links between docs are valid
- [ ] All variable names match actual source files (grep to verify)
- [ ] All tag names verified via `ansible-playbook --list-tags`
- [ ] All distribution names verified from vars files
- [ ] No placeholder text like "TODO" or "TBD" remains (unless source is genuinely missing)
- [ ] Each documented command can be executed without error
- [ ] No content was invented without source file backing

### Post-Generation Verification Commands

```bash
# Verify all documented variables exist
grep -r "variable_name" packages/ansible/

# Verify all documented tags exist
ansible-playbook --list-tags -i packages/ansible/inventory/localhost.yml packages/ansible/playbooks/bootstrap.yml

# Syntax check all example commands
ansible-playbook --syntax-check -i packages/ansible/inventory/localhost.yml packages/ansible/playbooks/bootstrap.yml
```

---

## Execution Order

1. **Discovery Phase** (NO writing yet)
   - Read ALL source files listed in "Source Files Reference"
   - Run ALL verification commands in "Verification Commands" section
   - Build internal knowledge of actual project state

2. **Structure Creation**
   - Create directory structure

3. **Write Phase** (in order)
   - `docs/architecture/` (foundational understanding)
   - `docs/reference/` (factual data extraction)
   - `README.md` and `docs/index.md` (now that you know what exists)
   - `docs/getting-started/`
   - `docs/guides/`
   - `docs/examples/`

4. **Validation Phase**
   - Run all validation checklist items
   - Fix any discrepancies found

---

## Forbidden Actions

1. **DO NOT** document roles that don't exist in the filesystem
2. **DO NOT** document variables that aren't defined in source files
3. **DO NOT** document tags that don't appear in playbooks
4. **DO NOT** assume ansible "best practices" apply if not visible in code
5. **DO NOT** add features, improvements, or suggestions to documentation
6. **DO NOT** document future plans unless explicitly written in source comments
7. **DO NOT** use phrases like "typically", "usually", "commonly", "generally" to mask uncertainty
8. **DO NOT** proceed if a source file cannot be read - report the issue instead
