import argparse
import csv
import json
from pathlib import Path
from datetime import datetime

def get_latest_stage_results(log_dir):
    """Get the most recent result for each migration item across all jobs."""
    latest_results = {}
    
    # Process all JSON files in log directory
    for json_file in Path(log_dir).glob('*.json'):
        with open(json_file) as f:
            try:
                results = json.load(f)
                # Extract jobid and stage from filename
                jobid = json_file.stem.split('_')[0]
                stage = '_'.join(json_file.stem.split('_')[1:])
                
                for item in results:
                    name = item['name']
                    timestamp = item.get('timestamp', '')
                    
                    # Update if this is the first or a more recent result
                    if name not in latest_results or timestamp > latest_results[name]['timestamp']:
                        latest_results[name] = {
                            'status': item['status'],
                            'last_jobid': jobid,
                            'last_stage': stage,
                            'timestamp': timestamp
                        }
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {json_file}")
                continue
    
    return latest_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-dir', required=True, help='Directory containing log files')
    parser.add_argument('--output', required=True, help='Output CSV file path')
    args = parser.parse_args()
    
    # Read current migrations.csv
    migrations = {}
    try:
        with open(args.output, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                migrations[row['name']] = row
    except FileNotFoundError:
        print(f"Warning: {args.output} not found, will create new file")
    
    # Get latest results from log files
    latest_results = get_latest_stage_results(args.log_dir)
    
    # Update migrations with latest results
    for name, result in latest_results.items():
        # Find matching name case-insensitively
        matching_name = next(
            (n for n in migrations.keys() if n.lower() == name.lower()),
            None
        )
        if matching_name:
            migrations[matching_name].update({
                'status': result['status'],
                'last_jobid': result['last_jobid'], 
                'last_stage': result['last_stage'],
                'last_updated': result['timestamp']
            })
    
    # Write updated migrations.csv
    with open(args.output, 'w', newline='') as f:
        fieldnames = ['name', 'status', 'last_jobid', 'last_stage', 'last_updated']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for name in sorted(migrations.keys()):
            writer.writerow(migrations[name])

if __name__ == '__main__':
    main()