# Day 2 - Lists, Tuples, and Interation
# A list is an ordered collection of items
user_ids = ["USR_001", "USR_002", "USR_003", "USR_004", "USR_005"]
query_counts = [847, 23, 1205, 4, 389]
#Basic list operations
print(user_ids)
print(user_ids[0])
print(user_ids[1])
print(user_ids[-1])
print(len(user_ids))

# Modifying lists
user_ids.append("USR_006")
print(user_ids)
user_ids.remove("USR_002")
print(user_ids)
user_ids[0] = "USR_000"
print(user_ids)
print(len(user_ids))

# Looping through a list
print("\n--- Loop Examples ---")
for user in user_ids:
    print(user)

# Loop with index
print("\n--- Loop with index ---")
for i, user in enumerate(user_ids):
    print(f"Position {i}: {user}")

#Loop with condition
print("\n--- Flagged Users ---")
flagged = ["USR_003", "USR_005"]
for user in user_ids:
    if user in flagged:
        print(f"{user} is FLAGGED")
    else:
        print(f"{user} is clear")

# Dictionaries - key/value pairs
print("\n--- Dictionaries ---")
account = {
    "user_id": "USR_003",
    "query_count": 1205,
    "risk_score": 8.7,
    "flagged": True,
    "country": "Unknown"
}

# Accessing values
print(account["user_id"])
print(account["query_count"])
print(f"Risk score for {account['user_id']}: {account['risk_score']}")
 
#Adding and updating values
account["status"] = "under review"
account["query_count"] = 1350
print(account)  

# Looping through a dictionary
print("\n--- Dictionary Loop ---")
for key, value in account.items():
    print(f"{key}: {value}")

# A list of dictionaries -- how real account data looks
print("\n--- Multiple Accounts ---")
accounts = [
    {"user_id": "USR_000", "query_count": 847, "risk_score": 3.2},
    {"user_id": "USR_003", "query_count": 1350, "risk_score": 8.7},
    {"user_id": "USR_004", "query_count": 4, "risk_score": 0.1},
    {"user_id": "USR_005", "query_count": 389, "risk_score": 6.5},
    {"user_id": "USR_006", "query_count": 23, "risk_score": 1.2},
    {"user_id": "USR_007", "query_count": 2750, "risk_score": 9.5},
]

# Find high risk accounts
print("\n--- High Risk Accounts ---")
for account in accounts:
    if account["risk_score"] >= 6.0:
        print(f"HIGH RISK: {account['user_id']} "
              f"(score: {account['risk_score']}, "
              f"queries: {account['query_count']})")    

# Tuples
print("\n--- Tuples ---")

CBRN_CATEGORIES = ("Chemical", "Biological", "Radiological", "Nuclear", "Explosive")

print(CBRN_CATEGORIES)
print(CBRN_CATEGORIES[0])
print(len(CBRN_CATEGORIES))

#L Loop through tuple same as list
for category in CBRN_CATEGORIES:
    print(f"Category: {category}")

# Tuple unpacking
lat, lon = (38.8977, -77.0365)
print(f"Washington DC is at {lat}, {lon}")

# Conditional logic
print("\n--- Conditional Logic ---")

def classify_risk(score):
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 5.0:
        return "Medium"
    elif score >= 2.0:
        return "Low"
    else:
        return "Normal"
    
# Test it against all accounts
for account in accounts:
    risk_tier = classify_risk(account["risk_score"])
    print(f"{account['user_id']}: {risk_tier} (score: {account['risk_score']})")