# Day 8 - Regular Expressions
import re
import pandas as pd

# Basic pattern matching
print("--- Basic Regex ---")

text = "User USR_003 made 47 queries from IP 192.168.1.1 at 02:15:00"

# Search for a pattern
match = re.search(r'\d+', text)
print(f"First number found: {match.group()}")

# Find ALL matches
all_numbers = re.findall(r'\d+', text)
print(f"All numbers found: {all_numbers}")

# Find IP address pattern
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ip_match = re.findall(ip_pattern, text)
print(f"IP address found: {ip_match}")

# Practical investigation patterns
print("\n--- Investigation Patterns ---")

log_entries = [
    "2024-06-15 02:15:00 USR_003 query from 192.168.1.1",
    "2024-06-15 09:30:00 USR_001 query from 72.21.91.1",
    "2024-06-15 02:17:45 USR_007 query from 10.0.0.1",
    "ERROR: invalid request from USR_004 at 2024-06-16 14:22:00",
    "2024-06-15 02:19:00 USR_007 query from 10.0.0.1",
]

# Extract all user IDs
user_pattern = r'USR_\d{3}'
for entry in log_entries:
    users = re.findall(user_pattern, entry)
    if users:
        print(f"Users found: {users} in: '{entry[:40]}...'")

# Extract all timestamps
print("\n--- Timestamps ---")
timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
for entry in log_entries:
    timestamps = re.findall(timestamp_pattern, entry)
    if timestamps:
        print(f"Timestamp: {timestamps[0]}")

# Extract all IP addresses
print("\n--- IP Addresses ---")
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
all_ips = []
for entry in log_entries:
    ips = re.findall(ip_pattern, entry)
    all_ips.extend(ips)
print(f"All IPs found: {all_ips}")
print(f"Unique IPs: {list(set(all_ips))}")

# Named groups and text cleaning
print("\n--- Named Groups ---")

# Named groups let you extract specific parts by name
log = "2024-06-15 02:15:00 USR_003 query from 192.168.1.1"

pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<user>USR_\d{3}) query from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
match = re.search(pattern, log)
if match:
    print(f"Timestamp: {match.group('timestamp')}")
    print(f"User:      {match.group('user')}")
    print(f"IP:        {match.group('ip')}")

# Text substitution -- redacting sensitive data
print("\n--- Text Redaction ---")
sensitive = "User USR_003 connected from 192.168.1.1 at 02:15:00"
redacted = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '[REDACTED IP]', sensitive)
print(f"Original: {sensitive}")
print(f"Redacted: {redacted}")