# scripts/run_migration.py
import sys
import csv
import json
import random
import time
from datetime import datetime
from pathlib import Path

def run_stage(name, stage):
    """Run a migration stage for a given item."""
    delay = random.randint(10, 30)
    time.sleep(delay)
    return random.random() > 0.33  # 66% success rate per item

def main():
    names = sys.argv[1].split(',')
    jobid = sys.argv[2]
    current_stage = sys.argv[3]
    
    Path('log').mkdir(exist_ok=True)
    
    # Load previous stage results if not first stage
    successful_items = set(names)
    
    # Process current stage
    results = []
    timestamp = datetime.now().isoformat()
    
    with open(f'log/{jobid}.log', 'a') as logfile:
        for name in names:
            if name in successful_items:
                success = run_stage(name, current_stage)
                status = 'success' if success else 'failed'
                logfile.write(f'{timestamp} - {name} - {current_stage}: {status}\n')
            else:
                status = 'skipped'
                logfile.write(f'{timestamp} - {name} - {current_stage}: skipped (failed in previous stage)\n')
            
            results.append({
                'name': name,
                'status': status,
                'jobid': jobid,
                'stage': current_stage,
                'timestamp': timestamp
            })
    
    # Save stage results to JSON
    with open(f'log/{jobid}_{current_stage}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Update per-job CSV
    fieldnames = ['name', 'status', 'last_jobid', 'last_stage', 'last_updated']
    job_csv_path = f'log/{jobid}.csv'
    
    try:
        with open(job_csv_path, 'r') as f:
            existing_results = list(csv.DictReader(f))
            existing_data = {row['name']: row for row in existing_results}
    except FileNotFoundError:
        existing_data = {}
    
    with open(job_csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            # Only update last_stage if current status is success or failed
            row = existing_data.get(result['name'], {
                'name': result['name'],
                'status': 'pending',
                'last_jobid': '',
                'last_stage': '',
                'last_updated': ''
            })
            
            if result['status'] in ['success', 'failed']:
                row.update({
                    'status': result['status'],
                    'last_jobid': result['jobid'],
                    'last_stage': result['stage'],
                    'last_updated': result['timestamp']
                })
            
            writer.writerow(row)

if __name__ == '__main__':
    main()