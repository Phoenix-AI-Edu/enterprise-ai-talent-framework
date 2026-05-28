#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_config.py — 鳳凰 AI 簡報設定檔編譯前驗證器
========================================================================
Phoenix AI Slides Config Pre-compile Validator

目的：
  在 compile_slides.py 編譯「之前」先把關 JSON 設定檔，攔住三類問題：
    1. 【結構錯誤】缺必填欄位、型別錯誤、layout 不在白名單 —— 硬性，必擋。
    2. 【品質警告】字數超載、空的 speaker_notes、layout 太單調 —— 軟性，提醒。
    3. 【數量門檻】slides 數量低於 min_slides_required —— 硬性，必擋。

設計哲學（與 de_identify_local.py 一致）：
  - 「零相依可跑」：優先使用 jsonschema 套件做標準驗證；若環境未安裝，
    自動 fallback 到內建的純標準庫驗證器，確保任何顧問的電腦都能跑。
  - 「友善報錯」：錯誤訊息必須明確指出「第幾頁、哪個欄位、錯在哪」，
    而不是吐一個看不懂的 traceback。
  - 「可串接」：以 exit code 回報結果（0=通過 / 2=結構錯誤 / 3=僅品質警告），
    讓編譯流程或 CI 可據此決定是否繼續。

用法：
  python validate_config.py scripts/slides_config_yuepin.json
  python validate_config.py config.json --schema scripts/slides_config.schema.json
  python validate_config.py config.json --max-chars 250 --strict-notes
  python validate_config.py config.json --warnings-as-errors   # 品質警告也視為失敗

退出碼：
  0  全部通過（含僅有資訊性提示）
  2  發現結構性錯誤（必修，不可編譯）
  3  結構通過但有品質警告（可編譯，但建議修；加 --warnings-as-errors 則視為失敗）
========================================================================
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_SCHEMA = Path(__file__).parent / "slides_config.schema.json"

# 每種 layout 的必填欄位（fallback 驗證器使用；須與 schema 保持同步）
LAYOUT_REQUIRED = {
    "cover": ["title", "subtitle"],
    "dual-track": [
        "title", "badge_left", "title_left", "content_left",
        "badge_right", "title_right", "content_right",
    ],
    "interactive-roi": [
        "title", "slider_min", "slider_max",
        "slider_default", "cost_base", "num_workers",
    ],
    "interactive-roadmap": ["title", "tabs"],
    "next-steps": [
        "title",
        "card1_title", "card1_desc",
        "card2_title", "card2_desc",
        "card3_title", "card3_desc",
        "closing_quote", "consultants",
    ],
}

# 全部已知的合法欄位（用於 additionalProperties:false 的 fallback 模擬）。
# 須與 schema 的 slide.properties 鍵集合保持一致。
KNOWN_SLIDE_FIELDS = {
    "page", "layout", "progress_label", "speaker_notes",
    "title", "subtitle", "version", "date",
    "badge_left", "title_left", "content_left",
    "badge_right", "title_right", "content_right",
    "intro_text", "translation_box",
    "slider_min", "slider_max", "slider_default",
    "cost_base", "num_workers", "tabs",
    "card1_title", "card1_desc", "card2_title", "card2_desc",
    "card3_title", "card3_desc", "closing_quote", "consultants",
}
VALID_LAYOUTS = set(LAYOUT_REQUIRED.keys())

# 內容型欄位（用於字數品質檢查）
CONTENT_FIELDS = [
    "content_left", "content_right", "intro_text",
    "subtitle", "translation_box",
    "card1_desc", "card2_desc", "card3_desc",
]


class Issue:
    """單一問題：level 為 'error' 或 'warning'。"""
    def __init__(self, level, where, message):
        self.level = level
        self.where = where
        self.message = message

    def __str__(self):
        icon = "❌" if self.level == "error" else "⚠️ "
        return f"  {icon} [{self.where}] {self.message}"


# ----------------------------------------------------------------------
# 結構驗證：優先 jsonschema，否則 fallback
# ----------------------------------------------------------------------

def validate_structure_jsonschema(config, schema):
    """使用 jsonschema 套件做完整驗證，回傳 Issue 清單。"""
    import jsonschema
    from jsonschema import Draft7Validator

    validator = Draft7Validator(schema)
    issues = []
    for err in sorted(validator.iter_errors(config), key=lambda e: list(e.path)):
        path = list(err.path)
        # 把路徑翻成人話：slides -> 第 N 頁 -> 欄位
        if len(path) >= 2 and path[0] == "slides":
            idx = path[1]
            page = _page_label(config, idx)
            field = path[2] if len(path) > 2 else "(整頁)"
            where = f"第 {page} 頁 / {field}"
        elif path:
            where = " / ".join(str(p) for p in path)
        else:
            where = "頂層"
        issues.append(Issue("error", where, err.message))
    return issues


def validate_structure_fallback(config):
    """純標準庫驗證器：在沒有 jsonschema 時提供等效的核心檢查。"""
    issues = []

    # 頂層必填
    for key in ("client_name", "output_dir", "min_slides_required", "slides"):
        if key not in config:
            issues.append(Issue("error", "頂層", f"缺少必填欄位「{key}」"))

    # output_dir 格式（資安：必須在 slides/ 下）
    out = config.get("output_dir", "")
    if out and not re.match(r"^slides/[A-Za-z0-9_\-]+/?$", out):
        issues.append(Issue(
            "error", "頂層 / output_dir",
            f"格式不符，必須形如 slides/[client]/（目前為「{out}」）"))

    # min_slides_required 型別
    msr = config.get("min_slides_required")
    if msr is not None and not isinstance(msr, int):
        issues.append(Issue(
            "error", "頂層 / min_slides_required",
            f"必須為整數（目前型別為 {type(msr).__name__}）"))

    # audience 模式（影響公開版級距規則）
    audience = config.get("audience", "internal")
    if audience not in ("internal", "public"):
        issues.append(Issue(
            "error", "頂層 / audience",
            f"只能是 internal 或 public（目前為「{audience}」）"))

    # 頂層多餘欄位（模擬 schema additionalProperties:false）
    allowed_top = {"audience", "client_name", "client_badge", "logo_text",
                   "output_dir", "theme", "min_slides_required", "slides"}
    for k in config:
        if k not in allowed_top:
            issues.append(Issue(
                "error", "頂層",
                f"未定義的欄位「{k}」（可能是拼寫錯誤；如需新增請先更新 schema）"))

    slides = config.get("slides")
    if not isinstance(slides, list):
        issues.append(Issue("error", "頂層 / slides", "必須為陣列"))
        return issues
    if len(slides) == 0:
        issues.append(Issue("error", "頂層 / slides", "陣列不可為空"))
        return issues

    # 逐頁檢查
    for i, slide in enumerate(slides):
        page = _page_label(config, i)
        loc = f"第 {page} 頁"

        if not isinstance(slide, dict):
            issues.append(Issue("error", loc, "投影片必須為物件"))
            continue

        layout = slide.get("layout")
        if "layout" not in slide:
            issues.append(Issue("error", loc, "缺少必填欄位「layout」"))
            continue
        if layout not in VALID_LAYOUTS:
            issues.append(Issue(
                "error", f"{loc} / layout",
                f"「{layout}」不是合法 layout，可選：{', '.join(sorted(VALID_LAYOUTS))}"))
            continue

        if "page" not in slide:
            issues.append(Issue("error", loc, "缺少必填欄位「page」"))
        elif not re.match(r"^[0-9]{2}$", str(slide.get("page", ""))):
            issues.append(Issue(
                "error", f"{loc} / page",
                f"必須為兩位數字串，如 01（目前為「{slide.get('page')}」）"))

        # 該 layout 的必填欄位
        for field in LAYOUT_REQUIRED[layout]:
            if field not in slide:
                issues.append(Issue(
                    "error", f"{loc} / {field}",
                    f"layout「{layout}」缺少必填欄位「{field}」"))
            elif isinstance(slide[field], str) and slide[field].strip() == "":
                issues.append(Issue(
                    "error", f"{loc} / {field}",
                    f"必填欄位「{field}」不可為空字串"))

        # slide 層多餘欄位（模擬 additionalProperties:false）
        for k in slide:
            if k not in KNOWN_SLIDE_FIELDS:
                issues.append(Issue(
                    "error", f"{loc} / {k}",
                    f"未定義的欄位「{k}」（可能是拼寫錯誤，如 closing_qoute）"))

        # interactive-roi 的數值型別與邏輯（依 audience 切換規則）
        if layout == "interactive-roi":
            _check_roi(slide, loc, issues, audience)

        # interactive-roadmap 的 tabs 結構
        if layout == "interactive-roadmap":
            _check_tabs(slide, loc, issues)

    return issues


def _check_roi(slide, loc, issues, audience="internal"):
    # slider 三項在兩種模式下都必須是數字
    for f in ("slider_min", "slider_max", "slider_default"):
        v = slide.get(f)
        if v is not None and not isinstance(v, (int, float)):
            issues.append(Issue(
                "error", f"{loc} / {f}",
                f"必須為數字（目前型別 {type(v).__name__}，常見錯誤是寫成字串 \"{v}\"）"))

    cost = slide.get("cost_base")
    nw = slide.get("num_workers")

    if audience == "public":
        # 公開版：禁止精確絕對值，必須為級距字串（防由精確值反推客戶身分）
        range_cost = re.compile(r"^[0-9]+\s*[-~–至]\s*[0-9]+\s*(?:萬|千|元|K|M)?$")
        range_num = re.compile(r"^[0-9]+\s*[-~–至]\s*[0-9]+\s*(?:人|家|店)?$")
        if cost is not None and not (isinstance(cost, str) and range_cost.match(cost)):
            issues.append(Issue(
                "error", f"{loc} / cost_base",
                f"公開版禁用精確值，必須為級距字串如 '40-50 萬'（目前為 {cost!r}）"))
        if nw is not None and not (isinstance(nw, str) and range_num.match(nw)):
            issues.append(Issue(
                "error", f"{loc} / num_workers",
                f"公開版禁用精確人數，必須為級距字串如 '400-500 家'（目前為 {nw!r}）"))
    else:
        # 內部/客戶版：cost_base 須為數字、num_workers 須為整數
        if cost is not None and not isinstance(cost, (int, float)):
            issues.append(Issue(
                "error", f"{loc} / cost_base",
                f"必須為數字（目前型別 {type(cost).__name__}，常見錯誤是寫成字串 \"{cost}\"）"))
        if nw is not None and not isinstance(nw, int):
            issues.append(Issue(
                "error", f"{loc} / num_workers",
                f"必須為整數（目前型別 {type(nw).__name__}）"))

    # 邏輯一致性（兩種模式皆檢查 slider）
    smin, smax = slide.get("slider_min"), slide.get("slider_max")
    sdef = slide.get("slider_default")
    if isinstance(smin, (int, float)) and isinstance(smax, (int, float)) and smin >= smax:
        issues.append(Issue(
            "error", f"{loc} / slider",
            f"slider_min({smin}) 必須小於 slider_max({smax})"))
    if (isinstance(sdef, (int, float)) and isinstance(smin, (int, float))
            and isinstance(smax, (int, float)) and not (smin <= sdef <= smax)):
        issues.append(Issue(
            "error", f"{loc} / slider_default",
            f"預設值 {sdef} 必須落在 [{smin}, {smax}] 區間內"))


def _check_tabs(slide, loc, issues):
    tabs = slide.get("tabs")
    if not isinstance(tabs, list):
        issues.append(Issue("error", f"{loc} / tabs", "必須為陣列"))
        return
    if len(tabs) < 2:
        issues.append(Issue(
            "error", f"{loc} / tabs",
            f"時程頁至少需 2 個分頁（目前 {len(tabs)} 個）"))
    for j, tab in enumerate(tabs):
        if not isinstance(tab, dict):
            issues.append(Issue("error", f"{loc} / tabs[{j}]", "分頁必須為物件"))
            continue
        for f in ("name", "content"):
            if f not in tab or (isinstance(tab.get(f), str) and not tab[f].strip()):
                issues.append(Issue(
                    "error", f"{loc} / tabs[{j}] / {f}",
                    f"分頁缺少或空白的「{f}」"))


def _page_label(config, idx):
    """取該頁的 page 欄位作為人類可讀標籤，取不到就用索引。"""
    try:
        return config["slides"][idx].get("page", f"#{idx + 1}")
    except Exception:
        return f"#{idx + 1}"


# ----------------------------------------------------------------------
# 軟性品質檢查（Schema 管不到的，呼應「不只擋數量、也看品質」）
# ----------------------------------------------------------------------

def quality_checks(config, max_chars, strict_notes):
    issues = []
    slides = config.get("slides", [])
    if not isinstance(slides, list):
        return issues

    # 1. 數量門檻（硬性 error）
    msr = config.get("min_slides_required")
    if isinstance(msr, int) and len(slides) < msr:
        issues.append(Issue(
            "error", "品質門檻",
            f"投影片僅 {len(slides)} 頁，低於 min_slides_required={msr}，"
            f"編譯器將中斷（杜絕偷工減料）"))

    layout_counter = {}
    for i, slide in enumerate(slides):
        if not isinstance(slide, dict):
            continue
        page = _page_label(config, i)
        loc = f"第 {page} 頁"
        layout = slide.get("layout")
        layout_counter[layout] = layout_counter.get(layout, 0) + 1

        # 2. 字數警戒線（軟性 warning）
        for f in CONTENT_FIELDS:
            v = slide.get(f)
            if isinstance(v, str):
                n = len(v.strip())
                if n > max_chars:
                    issues.append(Issue(
                        "warning", f"{loc} / {f}",
                        f"內容 {n} 字，超過密度警戒線 {max_chars} 字，"
                        f"建議精簡或拆頁"))

        # 3. 空的 speaker_notes（軟性 warning，--strict-notes 時升為 error）
        notes = slide.get("speaker_notes", "")
        if not isinstance(notes, str) or notes.strip() == "":
            level = "error" if strict_notes else "warning"
            issues.append(Issue(
                level, f"{loc} / speaker_notes",
                "缺少演講者注釋，現場簡報將無口訣可循"))

    # 4. layout 多樣性（軟性 warning）
    if slides:
        for layout, count in layout_counter.items():
            ratio = count / len(slides)
            if ratio > 0.6 and len(slides) >= 4:
                issues.append(Issue(
                    "warning", "整體版式",
                    f"layout「{layout}」占 {count}/{len(slides)} 頁（{ratio:.0%}），"
                    f"視覺可能單調，建議混用其他版式"))

    return issues


# ----------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="鳳凰 AI 簡報設定檔編譯前驗證器（結構 + 品質雙重把關）")
    parser.add_argument("config", help="待驗證的 slides_config JSON 路徑")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA),
                        help="JSON Schema 路徑（預設同目錄 slides_config.schema.json）")
    parser.add_argument("--max-chars", type=int, default=250,
                        help="單欄內容字數警戒線（預設 250）")
    parser.add_argument("--strict-notes", action="store_true",
                        help="將空的 speaker_notes 視為錯誤而非警告")
    parser.add_argument("--warnings-as-errors", action="store_true",
                        help="品質警告也視為失敗（退出碼 2）")
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        sys.exit(f"錯誤：找不到設定檔 {cfg_path}")

    # 載入 JSON（先擋語法錯誤）
    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print("❌ JSON 語法錯誤，無法解析：")
        print(f"   第 {e.lineno} 行第 {e.colno} 欄：{e.msg}")
        sys.exit(2)

    print(f"【設定檔驗證】{cfg_path}")

    # 結構驗證
    used_engine = "fallback（純標準庫）"
    try:
        schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
        struct_issues = validate_structure_jsonschema(config, schema)
        used_engine = "jsonschema（Draft-07）"
    except ImportError:
        struct_issues = validate_structure_fallback(config)
    except FileNotFoundError:
        print(f"   （找不到 schema 檔 {args.schema}，改用 fallback 驗證器）")
        struct_issues = validate_structure_fallback(config)

    print(f"   驗證引擎：{used_engine}\n")

    # 品質檢查
    qual_issues = quality_checks(config, args.max_chars, args.strict_notes)

    all_issues = struct_issues + qual_issues
    errors = [i for i in all_issues if i.level == "error"]
    warnings = [i for i in all_issues if i.level == "warning"]

    if errors:
        print(f"【結構 / 硬性錯誤】共 {len(errors)} 項（必修，不可編譯）")
        for it in errors:
            print(it)
        print()
    if warnings:
        print(f"【品質警告】共 {len(warnings)} 項（建議修）")
        for it in warnings:
            print(it)
        print()

    # 判定
    if errors:
        print("結論：❌ 驗證未通過，請修正上述硬性錯誤後再編譯。")
        sys.exit(2)
    if warnings:
        if args.warnings_as_errors:
            print("結論：❌ 結構通過，但因 --warnings-as-errors，品質警告視為失敗。")
            sys.exit(2)
        print("結論：⚠️  結構通過，可編譯；建議處理上述品質警告以提升交付水準。")
        sys.exit(3)
    print("結論：✅ 全部通過，可進行編譯。")
    sys.exit(0)


if __name__ == "__main__":
    main()
