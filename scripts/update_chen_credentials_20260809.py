#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Phoenix Chen academic credentials across site: de-specific school names per Owner.
Replace: 曾任南榮科技大學助理教授兼數位科技中心主任，現任高雄科技大學兼任助理教授
With:    曾任科技大學助理教授與數位科技中心主任，現兼任多所大學助理教授
Only touches Phoenix Chen (陳文家) credential lines. Meng Shu-Hui (孟淑慧) lines untouched.
"""
import io, re, sys

BASE = r"C:/Users/m1016/Documents/AI_Talent"

# (file, old, new) exact replacements for Chen's credential text
REPLACEMENTS = [
    # index.html main team card
    (r"index.html",
     "曾任南榮科技大學助理教授兼<strong>數位科技中心主任</strong>，現任<strong>高雄科技大學兼任助理教授</strong>",
     "曾任科技大學助理教授與<strong>數位科技中心主任</strong>，現兼任<strong>多所大學助理教授</strong>"),
    (r"index.html",
     "助理教授證書持有人、高科大兼任助理教授",
     "助理教授證書持有人、現兼任多所大學助理教授"),
    # m01.html
    (r"m01.html",
     "前南榮科大助理教授兼數位科技中心主任",
     "曾任科技大學助理教授與數位科技中心主任"),
    (r"m01.html",
     "高科大兼任助理教授，AI 架構與精算專家",
     "現兼任多所大學助理教授，AI 架構與精算專家"),
    # m02.html
    (r"m02.html",
     "高科大兼任助理教授，技術性安全防護欄 (Guardrails) 專家",
     "現兼任多所大學助理教授，技術性安全防護欄 (Guardrails) 專家"),
    # m03/m05/m06/m08/m09/m11/m13.html generic line
    (r"m03.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m05.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m06.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m08.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m09.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m11.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    (r"m13.html", "教育部助理教授，高科大兼任講師", "教育部助理教授，現兼任多所大學助理教授"),
    # README.md
    (r"README.md",
     "前南榮科技大學助理教授兼**數位科技中心主任**；現任**高雄科技大學兼任助理教授**",
     "曾任科技大學助理教授與**數位科技中心主任**；現兼任**多所大學助理教授**"),
    # curriculum/modules_landing_copy.md
    (r"curriculum/modules_landing_copy.md",
     "前南榮科技大學助理教授兼數位科技中心主任、現任高雄科技大學兼任助理教授",
     "曾任科技大學助理教授與數位科技中心主任、現兼任多所大學助理教授"),
    (r"curriculum/modules_landing_copy.md",
     "教育部助理教授，深諳台灣個資法與企業合規體系，高科大兼任助理教授。",
     "教育部助理教授，深諳台灣個資法與企業合規體系，現兼任多所大學助理教授。"),
    # curriculum/unit_8_grants/curriculum_v2026.md (section 8.6.2 Chen endorsement)
    (r"curriculum/unit_8_grants/curriculum_v2026.md",
     "### 8.6.2 大學產學合作通道與高科大 AI 中心",
     "### 8.6.2 大學產學合作通道與大學 AI 中心"),
    (r"curriculum/unit_8_grants/curriculum_v2026.md",
     "**陳文家策略長學術背書**：教育部認證助理教授、現任高雄科技大學兼任助理教授、前南榮科大數位科技中心主任。",
     "**陳文家策略長學術背書**：教育部認證助理教授、現兼任多所大學助理教授、曾任科技大學數位科技中心主任。"),
    (r"curriculum/unit_8_grants/curriculum_v2026.md",
     "企業可透過陳策略長，直接對接 **「高科大 AI 研究中心」** 或相關學術資源",
     "企業可透過陳策略長，直接對接 **「多所大學 AI 研究中心」** 或相關學術資源"),
    # slides/m12_government_grants/10-slide.html (Chen endorsement speech)
    (r"slides/m12_government_grants/10-slide.html",
     "我們的策略長陳文家是教育部認證助理教授，現任高科大助理教授。",
     "我們的策略長陳文家是教育部認證助理教授，現兼任多所大學助理教授。"),
    (r"slides/m12_government_grants/10-slide.html",
     "我們能直接調動高科大 AI 研究中心與 PMC 的法人資源。",
     "我們能直接調動大學 AI 研究中心與 PMC 的法人資源。"),
]

def fix_crlf(txt):
    return txt

changed = 0
errors = []
for rel, old, new in REPLACEMENTS:
    p = BASE + "/" + rel
    try:
        txt = io.open(p, encoding="utf-8").read()
    except Exception as e:
        errors.append(f"{rel}: read error {e}")
        continue
    if old in txt:
        n = txt.count(old)
        txt = txt.replace(old, new)
        io.open(p, "w", encoding="utf-8", newline="").write(txt)
        print(f"OK  {rel}: {n} replacement(s)")
        changed += 1
    else:
        print(f"--  {rel}: pattern NOT FOUND (may already be updated or line differs)")

print(f"\nTotal files changed: {changed}")
if errors:
    print("ERRORS:", errors)
    sys.exit(1)
