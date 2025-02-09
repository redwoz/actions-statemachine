import argparse
import csv
import json
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', required=True)
    parser.add_argument('--jobid', required=True)
    args = parser.parse_args()
    
    names = args.names.split(',')
    migration_items = []
    
    with open('migrations.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] in names:
                migration_items.append({
                    'name': row['name'],
                    'status': row['status'],
                    'jobid': args.jobid,
                    'timestamp': datetime.now().isoformat()
                })
    
    json.dump(migration_items, sys.stdout)

if __name__ == '__main__':
    main()