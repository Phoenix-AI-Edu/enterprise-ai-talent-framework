# -*- coding: utf-8 -*-
import os
import sys

# Force UTF-8 stdout if possible
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

csv_path = "curriculum/unit_7_strategy/phoenix_ai_expert_cases.csv"
if os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    cleaned_lines = []
    removed_count = 0
    for line in lines:
        if any(case_id in line for case_id in ["PHX-CASE-2026-034", "PHX-CASE-2026-035", "PHX-CASE-2026-036"]):
            removed_count += 1
            continue
        cleaned_lines.append(line)
        
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.writelines(cleaned_lines)
    print(f"Cleanup successful! Removed {removed_count} duplicate rows.")
else:
    print("CSV file not found!")
