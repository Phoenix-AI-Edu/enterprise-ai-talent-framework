# -*- coding: utf-8 -*-
import json

log_path = r"C:\Users\Ring\.gemini\antigravity\brain\d3f486ea-2ec7-4963-aee6-bca6d6343d02\.system_generated\logs\transcript.jsonl"
output_path = r"g:\我的雲端硬碟\AI_Talent\scripts\extracted_user_inputs.txt"

with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

user_inputs = []
for idx, line in enumerate(lines):
    try:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT":
            user_inputs.append(f"=== Request {idx} ===\n{data.get('content')}\n")
    except Exception as e:
        pass

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(user_inputs))

print("Successfully extracted user inputs to scripts/extracted_user_inputs.txt")
