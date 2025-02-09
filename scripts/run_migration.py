# scripts/run_migration.py
import sys
import csv
import json
import random
import time
from datetime import datetime
from pathlib import Path

def run_stage(name, stage):
    delay = random.randint(10, 30)
    time.sleep(delay)
    return random.random() > 0.25  # 75% success rate per item

def main():
    names = sys.argv[1].split(',')
    jobid = sys.argv[2]
    current_stage = sys.argv[3]  # Get current stage from command line
    stages = ['World 1-1', 'World 1-2', 'World 1-3']
    
    Path('log').mkdir(exist_ok=True)
    
    # Load previous stage results if not first stage
    stage_index = stages.index(current_stage)
    successful_items = set(names)
    
    if stage_index > 0:
        previous_stage = stages[stage_index - 1]
        previous_results_file = f'log/{jobid}_{previous_stage}.json'
        try:
            with open(previous_results_file, 'r') as f:
                previous_results = json.load(f)
                successful_items = {item['name'] for item in previous_results if item['status'] == 'success'}
        except FileNotFoundError:
            print(f"Warning: No results found for previous stage {previous_stage}")
    
    # Process current stage
    results = []
    with open(f'log/{jobid}.log', 'a') as logfile:
        for name in names:
            if name not in successful_items:
                status = 'skipped'
                timestamp = datetime.now().isoformat()
                logfile.write(f'{timestamp} - {name} - {current_stage}: skipped (failed in previous stage)\n')
            else:
                success = run_stage(name, current_stage)
                status = 'success' if success else 'failed'
                timestamp = datetime.now().isoformat()
                logfile.write(f'{timestamp} - {name} - {current_stage}: {status}\n')
            
            results.append({
                'name': name,
                'status': status,
                'jobid': jobid,
                'stage': current_stage,
                'timestamp': timestamp
            })
    
    # Save stage results
    with open(f'log/{jobid}_{current_stage}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Update main CSV with latest status
    with open(f'log/{jobid}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'status', 'last_jobid', 'last_stage', 'last_updated'])
        for result in results:
            writer.writerow([
                result['name'],
                result['status'],
                result['jobid'],
                result['stage'],
                result['timestamp']
            ])

if __name__ == '__main__':
    main()