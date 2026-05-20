import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

# --- Configuration ---
NUM_USERS = 500
NUM_ROWS = 50000
CBRN_KEYWORDS = ['synthesize', 'pathogen', 'fission', 'dispersal', 'compound', 'nuclear', 'precursor', 'transmission']
BENIGN_KEYWORDS = ['python', 'database', 'algorithm', 'network', 'security', 'testing', 'deployment']

# Randomly select user IDs for suspicious accounts
all_user_ids = [f'USR_{i:03d}' for i in range(1, NUM_USERS + 1)]
random.shuffle(all_user_ids)

suspicious_users = {
    'high_velocity': all_user_ids[0:5],
    'cbrn_focused': all_user_ids[5:8],
    'coordinated_ips': all_user_ids[8:12],
    'midnight_users': all_user_ids[12:14],
    'paraphrase_user': [all_user_ids[14]],
}

# Flatten to get all suspicious user IDs
all_suspicious = set()
for group in suspicious_users.values():
    all_suspicious.update(group)

print(f"Suspicious users: {sorted(all_suspicious)}")
print(f"Total suspicious: {len(all_suspicious)}, Normal: {NUM_USERS - len(all_suspicious)}")

# --- Step 2: Generate base query distributions ---
def generate_query(user_id):
    """Generate a query appropriate for the user type."""
    
    # High velocity users: random mix
    if user_id in suspicious_users['high_velocity']:
        keywords = random.choices(CBRN_KEYWORDS + BENIGN_KEYWORDS, k=random.randint(1, 3))
        return f"How to {' '.join(keywords)} {fake.word()}"
    
    # CBRN-focused users: heavily CBRN
    elif user_id in suspicious_users['cbrn_focused']:
        if random.random() < 0.7:  # 70% CBRN queries
            keywords = random.choices(CBRN_KEYWORDS, k=2)
            return f"Methods for {' '.join(keywords)}"
        else:
            return fake.sentence()
    
    # Coordinated users: identical or near-identical
    elif user_id in suspicious_users['coordinated_ips']:
        base_queries = [
            "How to extract chemical components",
            "Pathogen transmission methods",
            "Nuclear material enrichment",
            "Explosive device assembly"
        ]
        return random.choice(base_queries)
    
    # Midnight users: normal queries (behavior is in timestamps, not query text)
    elif user_id in suspicious_users['midnight_users']:
        return fake.sentence()
    
    # Paraphrase user: slight variations on same question
    elif user_id in suspicious_users['paraphrase_user']:
        base = "What is the chemical formula for"
        compounds = ['TATP', 'RDX', 'TNT', 'PETN']
        return f"{base} {random.choice(compounds)} and how to synthesize it"
    
    # Normal users: benign queries
    else:
        return fake.sentence()

# --- Step 3: Generate logs ---
logs = []
base_date = datetime(2024, 1, 1)

# Assign shared IPs to coordinated users
coordinated_ips = ['192.168.1.101', '192.168.1.102']
user_to_ip = {}
for i, user_id in enumerate(suspicious_users['coordinated_ips']):
    user_to_ip[user_id] = coordinated_ips[i % len(coordinated_ips)]

for i in range(NUM_ROWS):
    # Pick a random user
    if random.random() < 0.03:  # 3% chance of suspicious user for natural distribution
        user_id = random.choice(list(all_suspicious))
    else:
        user_id = f'USR_{random.randint(1, NUM_USERS):03d}'
    
    # Generate timestamp
    days_offset = random.randint(0, 180)
    hour = random.randint(0, 23)
    
    # Midnight users get more midnight queries
    if user_id in suspicious_users['midnight_users']:
        if random.random() < 0.5:
            hour = random.randint(0, 4)  # Heavy midnight activity
    
    timestamp = base_date + timedelta(days=days_offset, hours=hour, minutes=random.randint(0, 59))
    
    # Generate query and response length
    query_text = generate_query(user_id)
    
    # High velocity users get longer responses (more data transfer)
    if user_id in suspicious_users['high_velocity']:
        response_length = random.randint(2000, 5000)
    elif user_id in suspicious_users['cbrn_focused']:
        response_length = random.randint(1500, 3000)
    else:
        response_length = random.randint(500, 2000)
    
    # Assign IP address
    if user_id in user_to_ip:
        ip_address = user_to_ip[user_id]
    else:
        ip_address = fake.ipv4()
    
    logs.append({
        'user_id': user_id,
        'timestamp': timestamp,
        'query_text': query_text,
        'response_length': response_length,
        'ip_address': ip_address
    })

# --- Step 4: Create DataFrame and save ---
df = pd.DataFrame(logs)
df = df.sort_values('timestamp').reset_index(drop=True)
df.to_csv('data/capstone_logs_enhanced.csv', index=False)

print(f"\nDataset generated successfully!")
print(f"Shape: {df.shape}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Saved to: data/capstone_logs_enhanced.csv")

# --- Step 5: Quick sanity check ---
print("\nSuspicious user query counts:")
for user_id in sorted(all_suspicious):
    count = len(df[df['user_id'] == user_id])
    print(f"  {user_id}: {count} queries")