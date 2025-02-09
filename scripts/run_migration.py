# scripts/run_migration.py
import sys
import csv
import random
import time
from datetime import datetime
from pathlib import Path

def run_stage(name, stage):
    delay = random.randint(10, 30)
    time.sleep(delay)
    return random.random() > 0.25  # 75% success rate

def main():
    names = sys.argv[1].split(',')
    jobid = sys.argv[2]
    stages = ['World 1-1', 'World 1-2', 'World 1-3']
    
    Path('log').mkdir(exist_ok=True)
    
    with open(f'log/{jobid}.log', 'w') as logfile:
        results = []
        for name in names:
            for stage in stages:
                success = run_stage(name, stage)
                status = 'success' if success else 'failed'
                timestamp = datetime.now().isoformat()
                logfile.write(f'{timestamp} - {name} - {stage}: {status}\n')
                if not success:
                    break
            results.append([name, status, jobid, stage, timestamp])
    
    with open(f'log/{jobid}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'status', 'last_jobid', 'last_stage', 'last_updated'])
        writer.writerows(results)

if __name__ == '__main__':
    main()