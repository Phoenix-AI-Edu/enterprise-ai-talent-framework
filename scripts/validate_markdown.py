#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown Validator for 2026 Corporate AI Talent Curriculum
Author: Antigravity 2.0 (AG-2.0)
Date: 2026-05-21

This script automatically validates the curriculum markdown files against:
1. Heading hierarchy (Exactly one <h1> per file)
2. Specific terminology capitalization (e.g., RAG, Agent, MCP, ISO 42001, RLHF, DPO)
3. LaTeX Math Formula integrity (balanced delimiters $, $$)
"""

import os
import re
import sys

# Define standard terms and their correct cases
STANDARD_TERMS = {
    r"\brag\b": "RAG",
    r"\bmcp\b": "MCP",
    r"\bdpo\b": "DPO",
    r"\brlhf\b": "RLHF",
    r"\btokenizer\b": "Tokenizer",
    r"\btokenizers\b": "Tokenizers",
    r"\bembedding\b": "Embedding",
    r"\bembeddings\b": "Embeddings",
    r"\biso\s*42001\b": "ISO/IEC 42001",
    r"\biso/iec\s*42001\b": "ISO/IEC 42001",
    r"\bnist\s*ai\s*rmf\b": "NIST AI RMF",
    r"\bmultiagent\b": "Multiagent",
    r"\bmulti-agent\b": "Multiagent",
    r"\bdiscriminative\s*ai\b": "Discriminative AI",
    r"\bgenerative\s*ai\b": "Generative AI",
    r"\bhuman-in-the-loop\b": "Human-in-the-loop",
}

def check_file(file_path):
    print(f"[INFO] Analyzing: {os.path.relpath(file_path)}")
    errors = []
    warnings = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()
    except Exception as e:
        return [f"Failed to read file: {e}"], []

    # 1. Heading Hierarchy Check
    h1_count = 0
    h1_line = 0
    for idx, line in enumerate(lines, 1):
        if line.strip().startswith("# "):
            h1_count += 1
            h1_line = idx
            
    if h1_count == 0:
        errors.append("[ERROR] Missing <h1> (# heading). Every file must have exactly one <h1> heading.")
    elif h1_count > 1:
        errors.append(f"[ERROR] Multiple <h1> (# heading) found. Every file must have exactly one <h1> heading. Found {h1_count} headings.")

    # 2. Standard Terminology Check
    for pattern, correct_form in STANDARD_TERMS.items():
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            found_word = match.group(0)
            if found_word != correct_form:
                start_char = match.start()
                line_no = content[:start_char].count("\n") + 1
                warnings.append(
                    f"[WARN] Line {line_no}: Terminology capitalization warning. Found '{found_word}', suggest standard '{correct_form}'."
                )

    # 3. LaTeX Math Delimiter Balance Check
    # Pre-clean inline code and code blocks to prevent counting false positives inside backticks
    cleaned_content = re.sub(r"`[^`\n]+`", "", content) # inline code
    cleaned_content = re.sub(r"```.*?```", "", cleaned_content, flags=re.DOTALL) # code blocks

    # Clean currency patterns (e.g., NT$ 50,000, US$100, NT$) so they aren't confused with math delimiters
    # Matches currency prefixes followed by a dollar sign (e.g. NT$, US$, HK$)
    cleaned_content = re.sub(r"\b(?:NT|US|HK|RMB|GB|CA|AUD|EUR)\$", "", cleaned_content)


    # Count double dollar first on the cleaned content
    double_dollar_count = cleaned_content.count("$$")
    if double_dollar_count % 2 != 0:
        errors.append("[ERROR] Unbalanced LaTeX double dollar '$$' blocks. Formulas might render incorrectly.")
        
    # Remove double dollars before checking single dollars to prevent interference
    cleaned_content_no_double = cleaned_content.replace("$$", "")
    
    single_dollar_count = cleaned_content_no_double.count("$")
    if single_dollar_count % 2 != 0:
        errors.append("[ERROR] Unbalanced LaTeX inline dollar '$' markers. Inline math might render incorrectly.")


    return errors, warnings

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    curriculum_dir = os.path.join(project_root, "curriculum")
    
    if not os.path.exists(curriculum_dir):
        print(f"[ERROR] Curriculum directory not found at: {curriculum_dir}")
        sys.exit(1)
        
    all_errors = 0
    all_warnings = 0
    validated_files = 0
    
    root_readme = os.path.join(project_root, "README.md")
    files_to_check = []
    if os.path.exists(root_readme):
        files_to_check.append(root_readme)
        
    for root, dirs, files in os.walk(curriculum_dir):
        for file in files:
            if file.endswith(".md"):
                files_to_check.append(os.path.join(root, file))
                
    print(f"[RUN] Starting Markdown Validation across {len(files_to_check)} files...\n")
    
    for file_path in files_to_check:
        errors, warnings = check_file(file_path)
        validated_files += 1
        
        if errors or warnings:
            for err in errors:
                print(f"  {err}")
                all_errors += 1
            for warn in warnings:
                print(f"  {warn}")
                all_warnings += 1
        else:
            print("  [OK] All checks passed!")
        print("-" * 50)
        
    print(f"\n[SUMMARY] Validation Results:")
    print(f"  Files Checked: {validated_files}")
    print(f"  Total Errors: {all_errors}")
    print(f"  Total Warnings: {all_warnings}")
    
    if all_errors > 0:
        print("\n[FAIL] Validation completed with errors. Please fix them before publishing.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] Validation completed successfully! Everything looks standard.")
        sys.exit(0)

if __name__ == "__main__":
    main()
