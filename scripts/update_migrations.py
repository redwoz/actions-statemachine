# scripts/update_migrations.py
import csv
from pathlib import Path
from datetime import datetime

def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))

def main():
    # Read all job CSVs
    results = {}
    for csv_file in Path('log').glob('*.csv'):
        for row in read_csv(csv_file):
            name = row['name']
            if name not in results or row['last_updated'] > results[name]['last_updated']:
                results[name] = row
    
    # Update main migrations.csv
    with open('migrations.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'status', 'last_jobid', 'last_stage', 'last_updated'])
        for row in results.values():
            writer.writerow([row['name'], row['status'], row['last_jobid'], 
                           row['last_stage'], row['last_updated']])

if __name__ == '__main__':
    main()