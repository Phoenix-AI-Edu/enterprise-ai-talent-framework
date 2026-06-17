import re

csv_path = "curriculum/unit_7_strategy/phoenix_ai_expert_cases.csv"

print(f"Reading CSV file from {csv_path}...")
with open(csv_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
removed_count = 0

for line in lines:
    # Check if the line starts with any of the duplicate case IDs we want to remove
    if re.match(r"^PHX-CASE-2026-03[456],", line):
        print(f"Removing duplicate line: {line[:100]}...")
        removed_count += 1
    else:
        new_lines.append(line)

print(f"Total lines read: {len(lines)}")
print(f"Total lines removed: {removed_count}")
print(f"Total lines to write: {len(new_lines)}")

with open(csv_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("CSV cleanup complete successfully!")
