# create_initial_migrations.py
import csv
from datetime import datetime

characters = [
    "Mario", "Luigi", "Princess Peach", "Bowser", "Yoshi",
    "Toad", "Wario", "Waluigi", "DonkeyKong", "KoopaTroopa"
]

with open('migrations.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'status', 'last_jobid', 'last_stage', 'last_updated'])
    for char in characters:
        writer.writerow([char, 'pending', '', '', ''])