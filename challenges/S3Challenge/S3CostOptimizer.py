import json
from datetime import datetime
from collections import defaultdict

# load json (save your file as buckets.json)
with open('buckets.json') as f:
    data = json.load(f)

buckets = data['buckets']

# Config
COST_PER_GB = 0.023
TODAY = datetime.now().date()
UNUSED_THRESHOLD_DAYS = 90

summary = []
large_unused = []
cost_report = defaultdict(lambda: defaultdict(float))
cleanup_list = []
deletion_queue = []
archive_candidates = []

print("\n==== S3 Cost Optimization Report ====\n")
for bucket in buckets:
    name = bucket['name']
    region = bucket['region']
    size = bucket['sizeGB']
    versioning = bucket['versioning']
    team = bucket["tags"]["team"]

    # convert date
    created_date = datetime.strptime(bucket['createdOn'], '%Y-%m-%d').date()
    # created_date = datetime.strptime(b["createdOn"], "%Y-%m-%d").date()
    print(f"Processing bucket: {name} (created on {created_date})")
    age_days = (TODAY - created_date).days

    # Summary
    print(f"{name} | {region} | {size} GB | {versioning}" )

    # cost report    
    cost = size * COST_PER_GB
    cost_report[region][team] += cost

    # cleanup recommendations
    if size > 50:
        cleanup_list.append(name)

    # deletion candidates
    if size >100 and age_days > 20:
        deletion_queue.append(name)

    # archive candidates
    if size > 50 and size <= 100:
        archive_candidates.append(name)
    

    print(f"\n === cost report ====")
    for b in large_unused:
            print(b)
    
    for region, teams in cost_report.items():
         for team, cost in teams.items():
              print(f"{region} | {team} | ${cost:.2f}")
    
    # cleanup recommendations
    print(f"\n === Below Buckets are candidates for cleanup (size > 50 GB).")
    for bucket in cleanup_list:        
        print(f"Bucket {bucket}")
    
    # deletion candidates
    for bucket in deletion_queue:
        print(f"Bucket {bucket} is a candidate for deletion (size > 100 GB and age > 90 days).")
    
    # archive candidates
    for bucket in archive_candidates:
        print(f"Bucket {bucket} is a candidate for archiving (size between 50 and 100 GB).")

    # final delete candidates
    for bucket in deletion_queue:
        print(f"Bucket {bucket} is a candidate for final deletion (size > 100 GB and age > 90 days).")