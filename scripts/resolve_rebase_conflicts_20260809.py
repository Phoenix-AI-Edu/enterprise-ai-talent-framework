#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve rebase conflicts for website integration (RAG remote + Ledger/AOS local)."""
import io, re, sys

def read(p):
    return io.open(p, encoding='utf-8').read()

def write(p, txt):
    io.open(p, 'w', encoding='utf-8', newline='').write(txt)
    print('wrote', p)

# ---- 1. contact.html: merge both intent additions (keep all) ----
p = 'contact.html'
txt = read(p)
# conflict 1: intentLabels -> keep HEAD (RAG) + MINE (Ledger/AOS)
txt = txt.replace(
    "      central_kitchen_demo: '中央廚房營運防護台 Demo',\n<<<<<<< HEAD\n"
    "      rag_foundation_demo: 'Enterprise RAG Foundation 示範',\n"
    "      rag_foundation_assessment: '鳳凰企業 RAG Foundation 導入評估',\n"
    "=======\n"
    "      ledger_assist_demo: 'Ledger-Assist Demo',\n"
    "      capital_sprint_info: 'Capital Decision Sprint 說明',\n"
    ">>>>>>> c8afe1b (feat(website): publish ledger-assist & ai-allocation-os solution pages (v20260809-1))\n",
    "      central_kitchen_demo: '中央廚房營運防護台 Demo',\n"
    "      rag_foundation_demo: 'Enterprise RAG Foundation 示範',\n"
    "      rag_foundation_assessment: '鳳凰企業 RAG Foundation 導入評估',\n"
    "      ledger_assist_demo: 'Ledger-Assist Demo',\n"
    "      capital_sprint_info: 'Capital Decision Sprint 說明',\n"
)
# conflict 2: campaignIntent -> keep HEAD (RAG) + MINE (Ledger/AOS)
txt = txt.replace(
    "    central_kitchen_demo: 'central_kitchen_demo',\n<<<<<<< HEAD\n"
    "    rag_foundation_v1: 'rag_foundation_demo',\n"
    "    enterprise_rag_foundation: 'rag_foundation_demo'\n"
    "=======\n"
    "    ledger_assist_demo: 'ledger_assist_demo',\n"
    "    capital_sprint: 'capital_sprint_info'\n"
    ">>>>>>> c8afe1b (feat(website): publish ledger-assist & ai-allocation-os solution pages (v20260809-1))\n",
    "    central_kitchen_demo: 'central_kitchen_demo',\n"
    "    rag_foundation_v1: 'rag_foundation_demo',\n"
    "    enterprise_rag_foundation: 'rag_foundation_demo',\n"
    "    ledger_assist_demo: 'ledger_assist_demo',\n"
    "    capital_sprint: 'capital_sprint_info'\n"
)
# safety: if exact replace failed, fall back to regex-based merge
if '<<<<<<<' in txt:
    print('WARN: contact.html still has markers, trying generic merge')
    def merge_conflict(m):
        head = m.group(1)
        mine = m.group(2)
        # intent additions: merge both sides
        return head.rstrip('\n') + '\n' + mine.rstrip('\n') + '\n'
    txt = re.sub(r'<<<<<<< HEAD(.*?)=======(.*?)>>>>>>> [^\n]*\n', merge_conflict, txt, flags=re.S)
write(p, txt)

# ---- 2. experience/index.html: version param -> mine ----
p = 'experience/index.html'
txt = read(p)
txt = txt.replace('<<<<<<< HEAD\n<script src="./solutions_data.js?v=20260727-rag2"></script>\n=======\n<script src="./solutions_data.js?v=20260809-1"></script>\n>>>>>>> c8afe1b (feat(website): publish ledger-assist & ai-allocation-os solution pages (v20260809-1))',
                  '<script src="./solutions_data.js?v=20260809-1"></script>')
write(p, txt)

# ---- 3. experience/solutions_data.js: merge RAG (HEAD) + Ledger/AOS (MINE) ----
p = 'experience/solutions_data.js'
txt = read(p)
# Find conflict block: HEAD has enterprise_rag_foundation entry, MINE has ledger_assist + ai_allocation_os
m = re.search(r'<<<<<<< HEAD(.*?)=======(.*?)>>>>>>> [^\n]*\n', txt, re.S)
if m:
    rag_entry = m.group(1).rstrip('\r\n')
    my_entries = m.group(2).rstrip('\r\n')
    # The conflict sits between phoenix_auditable entry and the array close.
    # HEAD ends the RAG entry with '}' (no comma) before the array close; MINE is ledger entry + aos entry ending with '}'.
    # Correct JS: rag_entry needs trailing comma since more entries follow.
    merged = rag_entry.rstrip() + ',\n  ' + my_entries.lstrip()
    # my_entries already contains both entries separated correctly; ensure ends without trailing comma issue handled below
    txt = txt[:m.start()] + merged + txt[m.end():]
    # Ensure no double comma before array close
    txt = txt.replace('  }\n];', '  }\n];', 1)
write(p, txt)

# ---- 4. index.html: version param + slice -> mine ----
p = 'index.html'
txt = read(p)
txt = txt.replace('<<<<<<< HEAD\n<script src="./experience/solutions_data.js?v=20260727-rag2"></script>\n=======\n<script src="./experience/solutions_data.js?v=20260809-1"></script>\n>>>>>>> c8afe1b (feat(website): publish ledger-assist & ai-allocation-os solution pages (v20260809-1))',
                  '<script src="./experience/solutions_data.js?v=20260809-1"></script>')
txt = txt.replace('<<<<<<< HEAD\n        .slice(0, 4);\n=======\n        .slice(0, 6);\n>>>>>>> c8afe1b (feat(website): publish ledger-assist & ai-allocation-os solution pages (v20260809-1))',
                  '        .slice(0, 6);')
write(p, txt)

# ---- Verify no markers remain ----
ok = True
for p in ['contact.html','experience/index.html','experience/solutions_data.js','index.html']:
    t = read(p)
    n = len(re.findall(r'<<<<<<<|=======|>>>>>>>', t))
    print(f'{p}: markers={n}')
    if n:
        ok = False
sys.exit(0 if ok else 1)
