# Actions State Machine

A GitHub Actions-based state machine that manages multi-stage migrations using GitHub's infrastructure for state management and execution.

## Overview

This project implements a multi-stage migration system where:
- Migrations are tracked in a central `migrations.csv` file
- Each migration job runs through 3 stages ("World 1-1", "World 1-2", "World 1-3")
- State is managed through Git branches and JSON/CSV log files
- Results are automatically merged back to main and status updated

## Key Components

### State Management
- `migrations.csv`: Master state file tracking all migration items
- `/log/*.json`: Per-stage execution results
- `/log/*.csv`: Per-job consolidated results
- `/log/*.log`: Detailed execution logs

### Workflows

#### Migrate Workflow ([.github/workflows/migrate.yml](.github/workflows/migrate.yml))
1. Accepts list of names to migrate
2. Creates unique job ID (YYMMDD.HHMMSS format)
3. Runs 3 sequential stages:
   - World 1-1
   - World 1-2
   - World 1-3
4. Each stage:
   - Only runs if previous stage succeeded
   - Has 66% success rate (for testing)
   - Takes 10-30 seconds per item
5. Creates feature branch for isolation
6. Auto-merges results back to main

#### Update Results Workflow ([.github/workflows/updateresults.yml](.github/workflows/updateresults.yml))
- Triggers on main branch updates
- Consolidates latest results from log files
- Updates master `migrations.csv`

### Scripts

- [scripts/run_migration.py](scripts/run_migration.py): Executes individual migration stages
- [scripts/update_results.py](scripts/update_results.py): Updates master state file
- [scripts/prepare_migration.py](scripts/prepare_migration.py): Prepares migration data
- [scripts/stage_runner.py](scripts/stage_runner.py): Simulates stage execution

## Usage

To start a new migration:

```sh
gh workflow run migrate --field names=Mario,Luigi,Bowser