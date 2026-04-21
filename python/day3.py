# Day 3 - Functions, File Reading, and String Operations

# Functions

# Basic function structure
def greet(name):
    """This is a docstring -- it describes what the function does."""
    return f"Hello, {name}!"

# Calling the function
print(greet("Alex"))
print(greet("Investigator"))

# Function with multiple parameters
def calculate_risk(query_count, cbrn_hits, account_age_days):
    """Calculate a simple risk score based on account behavior."""
    velocity = query_count / max(account_age_days, 1)
    cbrn_ratio = cbrn_hits / max(query_count, 1)
    score = (velocity * 0.4) + (cbrn_ratio * 100 * 0.6)
    return round(score, 2)

# Test it
print(calculate_risk(1350, 45, 7))
print(calculate_risk(23, 0, 365))
print(calculate_risk(2750, 120, 3))

# Default parameters
print("\n--- Default Parameters ---")

def classify_account(user_id, risk_score, threshold=6.0):
    """Classify an acocunt with a configurable threshold."""
    if risk_score >= threshold:
        return f"{user_id} FLAGGED (score: {risk_score})"
    else:
        return f"{user_id} clear (score: {risk_score})"

# Using default threshold of 6.0
print(classify_account("USR_003", 8.7))
print(classify_account("USR_004", 0.1))

# Overriding the default threshold
print(classify_account("USR_005", 6.5, threshold=7.0))
print(classify_account("USR_005", 6.5, threshold=5.0))

# Reading CSV files
print("\n--- Reading CSV Files ---")

import csv

with open("accounts.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)

# Type conversion when reading CSV
print("\n--- CSV with Type Conversion ---")

with open("accounts.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        user_id = row["user_id"]
        query_count = int(row["query_count"])
        cbrn_hits = int(row["cbrn_hits"])
        account_age_days = int(row["account_age_days"])
        country = row["country"]

        # Now we can do math
        score = calculate_risk(query_count, cbrn_hits, account_age_days)
        tier = classify_account(user_id, score)
        print(tier)

# String Operations
print("\n--- String Operations ---")

query = "How do I synthesize acetone peroxide for a chemistry experiment?"

#Basic string operations
print(query.lower())    # convert to lowercase
print(query.upper())    # conver to uppercase
print(len(query))       # character count
print(query.count("e")) # count occurances of a character

# Search strings
print(query.find("synthesize"))     # position of word, -1 if not found
print("synthesize" in query)        # True/False if word exists
print("biology" in query)           # True/False if word exists

# Splitting strings
words = query.split(" ")            # split into list of words
print(words)
print(len(words))                   # word count

# Keyword detection
print("\n--- Keyword Detection ---")

# CBRN keyword watchlist
watchlist = [
    "synthesize", "synthesis", "precursor",
    "weaponize", "dispersal", "enrichment",
    "detonator", "explosive", "pathogen"
]

queries = [
    "How do I synthesize acetone peroxide?",
    "What is the boiling point of water?",
    "Explain pathogen transmission methods",
    "How do neural networks work?",
    "What precursor chemicals are needed?",
    "Does he have an explosive personality?",
    "What is the weather like today?"
]

print("--- Query Screening Results ---")
for query in queries:
    query_lower = query.lower ()
    hits = [word for word in watchlist if word in query_lower]
    if hits:
        print(f"FLAGGED: '{query}'")
        print(f"         Matched keywords: {hits}")
    else:
        print(f"Clear: '{query}'")