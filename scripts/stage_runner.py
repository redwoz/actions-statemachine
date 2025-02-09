import argparse
import json
import random
import time
from datetime import datetime

def run_stage(stage_name, data):
    delay = random.randint(10, 30)
    time.sleep(delay)
    success = random.random() > 0.25  # 75% success rate
    
    if not success:
        raise Exception(f"Stage {stage_name} failed")
    
    return success

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', required=True)
    parser.add_argument('--data', required=True)
    args = parser.parse_args()
    
    migration_data = json.loads(args.data)
    run_stage(args.stage, migration_data)

if __name__ == '__main__':
    main()