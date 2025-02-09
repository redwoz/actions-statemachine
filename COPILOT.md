I'm performing migrations and need to build a multi-stage state machine to manage the state of multiple migration items within a number of jobs. I'm wanting to do this in Python using GitHub Actions to perform the migration jobs and manage the state machine within the GitHub repository itself.

State management:
* consists of migrations.csv in the repository root with columns: name,status,last_jobid,last_updated (initialise with dummy data: name = 10 super mario characters, status = "pending", last_jobid = "", last_stage = "", last_updated = "")

GitHub Actions "migrate" workflow:
* accept a list of "name" which will be the migration items
* generate a jobid in the format "YYMMDD.HHmmSS"
* create a branch named "feature/$jobid" ($jobid from above point) for the current job run, using braches for each job run provides a way of concurrently running jobs and using merge to main to merge results
* workflow stages to individually iterate through the list of migration items and write a debug log to "/log/$jobid.log" ($jobid from above point)
* 3 basic workflow stages (initialise with dummy stages: use super mario levels), use dummy script (delay for between 10-30 seconds and fail on 1 in 4 runs for testing purposes)
* on completion of job run, write a new file "/log/$jobid.csv" containing only the lines from migrations.csv pertaining to the migration items being migrated in the job, updating the columns last_jobid,last_stage,last_updated
* merge back to main

GitHub Actions "autoupdate" workflow:
* triggers on merge to main
* updates migrations.csv from per-job CSV from /log, taking the most recent job update for each migration item

##############

step "Run Migration Stages" needs to trigger 3 separate external GitHub Actions workflows, each workflow accepting a JSON object which consists of the migration item information from migrations.csv
