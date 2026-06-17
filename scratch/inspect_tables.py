# -*- coding: utf-8 -*-
import os
import re
import sys

def inspect():
    cases = [
        'scripts/proposal_okayama_fastener.md',
        'scripts/proposal_okayama_forge.md',
        'scripts/proposal_okayama_heat.md',
        'scripts/proposal_okayama_cbam.md',
        'scripts/proposal_okayama_filter.md',
        'scripts/proposal_okayama_electroplate.md',
        'scripts/proposal_luzhu_coldheading.md',
        'scripts/proposal_okayama_barcode.md',
        'scripts/proposal_okayama_sbir.md'
    ]
    for path in cases:
        if not os.path.exists(path):
            print(f'{path} missing!')
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        tables = []
        lines = content.splitlines()
        in_table = False
        current_table = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('|') and stripped.endswith('|'):
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                if not in_table:
                    in_table = True
                    current_table = [cells]
                else:
                    current_table.append(cells)
            else:
                if in_table:
                    if len(current_table) > 1:
                        tables.append(current_table)
                    in_table = False
                    current_table = []
        if in_table and len(current_table) > 1:
            tables.append(current_table)
        
        print(f'File: {path}')
        print(f'  Total tables found: {len(tables)}')
        for idx, t in enumerate(tables, 1):
            headers_str = ''.join(t[0])
            if '痛點' in headers_str or '評估' in headers_str or '優先' in headers_str:
                print(f'  Table {idx} (Table 1: Scenario Inventory) columns:')
                print(f'    {t[0]}')
                print(f'    Rows count: {len(t)-1}')
                print(f'    First row key: "{t[1][0]}"')
            elif '路徑' in headers_str or '防線' in headers_str or '審計' in headers_str:
                print(f'  Table {idx} (Table 2: Solution Architecture) columns:')
                print(f'    {t[0]}')
                print(f'    First row key: "{t[1][0]}"')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    inspect()
