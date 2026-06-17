# -*- coding: utf-8 -*-
import os

BASE_DIR = r"g:\我的雲端硬碟\AI_Talent"
units = [
    {"dir": "unit_0_intro", "title": "單元 0：高階主管 AI 落地速覽 (CEO 90 分鐘決策課)"},
    {"dir": "unit_1_theory", "title": "單元一：AI 基礎理論與 2026 技術演進"},
    {"dir": "unit_2_industries", "title": "單元二：2026 企業級 AI 應用 7 大實戰模組"},
    {"dir": "unit_3_responsible_ai", "title": "單元三：負責任的 AI 應用 (Responsible AI)"},
    {"dir": "unit_4_machine_learning", "title": "單元四：中型企業機器學習實戰應用"},
    {"dir": "unit_5_explainable_ai", "title": "單元五：AI 可解釋性與信任度評估"},
    {"dir": "unit_6_generative_ai", "title": "單元六：生成式 AI 與多代理人系統 (Multiagent Systems)"},
    {"dir": "unit_7_strategy", "title": "單元七：企業 AI 導入、治理與營運策略"},
    {"dir": "unit_8_grants", "title": "單元八：AI 與台灣產業政策對接"}
]

def migrate():
    print("Starting Curriculum Handbook Migration...")
    
    for u in units:
        unit_path = os.path.join(BASE_DIR, "curriculum", u["dir"])
        readme_path = os.path.join(unit_path, "README.md")
        guide_path = os.path.join(unit_path, "instructor_guide.md")
        
        # 1. If local README.md exists, copy/rename it to instructor_guide.md (backstage private handbook)
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Only migrate if it contains instructor notes (to prevent overwriting already migrated files)
            if "逐字稿" in content or "時間管控" in content:
                with open(guide_path, "w", encoding="utf-8") as f_out:
                    f_out.write(content)
                print(f"  Backstage manual saved: {u['dir']}/instructor_guide.md")
            else:
                print(f"  {u['dir']}/README.md seems already clean, skipping backup.")
        
        # 2. Write a beautiful, clean, public-facing README.md for GitHub Pages (Open-Source Index Page)
        textbook_name = "curriculum_v2026.md"
        # Unit 0 doesn't have curriculum_v2026.md, it only has README.md
        has_textbook = os.path.exists(os.path.join(unit_path, textbook_name))
        
        public_readme = f"""# 📚 {u['title']}


歡迎來到「2026 企業級 AI 營運落地與人才培育開源框架」此單元課程首頁！

本教材嚴格對位經濟部與教育部之產業培訓標準，並融合 ISO/IEC 42001（人工智慧管理系統）與 NIST AI RMF（風險管理框架）之企業級實務架構。

---

## 🎯 學習目標與核心大綱

您可以在此單元中學習到企業級 AI 導入的商業脈絡、技術選型以及政策補助對接實務。本教材特別為現代企業經理人、數位轉型長（CDO）及 IT 架構主管提供客觀、客觀且具備實質 ROI 指引的系統化知識。

{"👉 **[📖 點此立即閱讀本單元公版標準教科書全文 (Markdown 格式)](" + textbook_name + ")**" if has_textbook else "👉 **[📖 點此返回課程首頁](../../README.md)**"}

---

## 💼 B2B 企業專屬解決方案

我們為轉型企業提供客製化、實戰化的落地輔導與工作坊方案：

* **方案 A：企業 AI 15 小時菁英培訓專班** ➔ 對位官方培訓標準，輔導企業完成內部能力建構。
* **方案 B：企業 AI 一頁式戰略畫布實戰工作坊** ➔ 孟顧問與陳策略長親自主持，帶領決策團隊完成「4+1 戰略畫布」與 90天行動計畫。
* **方案 C：ISO/IEC 42001 合規前期輔導** ➔ 針對高隱私與高度合規行業，建立 DLP 遮罩網閘與安全審計稽核日誌。

⚠️ **講師專屬資訊提示**：
> 本課程配有專屬的 **【講師幕後手冊（含 Slide-by-Slide 簡報大綱、版面設計與輪講逐字稿）】**，僅供簽約授權之企業內部講師及輔導顧問（孟顧問與陳策略長團隊）於後台教學備課使用，不向公眾開放。

---

✉️ **合作與諮詢對接**：
* 登記索取 Notion 資料庫協作模板工具包：**[📥 免費登記索取表單](https://docs.google.com/forms/d/e/1FAIpQLSfGlE4m-Tgg2AXcIGRy90jNuroTnt8ZGwB8r0E35msJIPw_xA/viewform)**
* 預約 30 分鐘專家線上快診諮詢或 B2B 內訓提案，請來信官方服務信箱：**allmyway2007@gmail.com**
"""
        with open(readme_path, "w", encoding="utf-8") as f_out:
            f_out.write(public_readme)
        print(f"  Public-facing README.md generated: {u['dir']}/README.md")
        
    print("All handbooks migrated successfully!")

if __name__ == "__main__":
    migrate()

