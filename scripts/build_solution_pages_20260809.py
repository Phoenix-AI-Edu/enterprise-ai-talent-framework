#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build solution pages for ledger-assist & ai-allocation-os from the central-kitchen template."""
import re, pathlib, argparse

BASE = pathlib.Path(r"C:/Users/m1016/Documents/AI_Talent/experience")

def build(target, container_html, solution_id, solution_title, hero_tag, meta_desc="可驗證的 AI 系統展示，能力邊界公開。"):
    src = (BASE / "central-kitchen-ai-agent" / "index.html").read_text(encoding="utf-8")
    # 0) target-specific canonical/OG/Twitter（避免繼承 central-kitchen metadata）
    canonical_url = f"https://03king.com/experience/{target}/"
    twitter_title = f"{solution_title}｜鳳凰 AI 顧問"
    src = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical_url}">',
        src, count=1)
    src = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="{canonical_url}">',
        src, count=1)
    src = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{twitter_title}">',
        src, count=1)
    src = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{meta_desc}">',
        src, count=1)
    # 1) title + meta description
    src = re.sub(
        r"<title>.*?</title>",
        f"<title>{solution_title}｜鳳凰 AI 顧問</title>",
        src, count=1, flags=re.S)
    src = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta_desc}">',
        src, count=1)
    src = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{solution_title}｜鳳凰 AI 顧問">',
        src, count=1)
    src = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{meta_desc}">',
        src, count=1)
    # 2) status badge text
    src = src.replace("公開沙盒示範", "對外展示", 1)
    # 3) replace container body between <div class="container"> and </div>\n\n  <footer
    start = src.index('<div class="container">')
    end = src.index('</div>\n\n  <footer')
    src = src[:start] + '<div class="container">\n' + container_html + '\n  </div>\n\n  <footer' + src[end + len('</div>\n\n  <footer'):]
    # 4) analytics script ids
    src = re.sub(r"var solutionId = '[^']*';", f"var solutionId = '{solution_id}';", src, count=1)
    src = re.sub(r"var solutionTitle = '[^']*';", f"var solutionTitle = '{solution_title}';", src, count=1)
    # 5) data-ga-solution-id on header badge
    src = re.sub(r'data-ga-solution-id="[^"]*"', f'data-ga-solution-id="{solution_id}"', src, count=1)
    out = BASE / target / "index.html"
    out.write_text(src, encoding="utf-8")
    print("wrote", out, len(src), "bytes")

# ── Ledger-Assist ──
ledger_container = """    <header class="page-header">
      <a href="../index.html" class="back-link">← 返回體驗區總覽</a>
      <div class="page-header-right">
        <div class="status-badge">
          <span class="status-dot"></span>
          Sandbox Demo
        </div>
        <span class="logo-mark">鳳凰 AI</span>
      </div>
    </header>

    <section class="hero">
      <div class="hero-glow"></div>
      <div class="hero-content">
        <div class="hero-tag">Accounting · LINE Workflow</div>
        <h1 class="hero-title">Ledger-Assist 發票收件與檢核系統</h1>
        <p class="hero-desc">客戶用 LINE 上傳發票，系統完成收件、辨識與檢核候選；事務所人員在 LINE 內修正、確認，經人工覆核核准後才匯出。正式憑證、帳務結果與稽核記錄，全部留在每家事務所獨立私有部署的環境——不是集中式帳務 SaaS。</p>
        <div class="hero-actions" id="hero-actions">
          <a href="../../contact.html?request_type=ledger_assist_assessment&amp;utm_source=site&amp;utm_medium=ledger_assist&amp;utm_campaign=ledger_assist_v2&amp;utm_content=hero" class="btn btn-primary" id="btn-demo-request-2">預約私有工作流程評估</a>
        </div>
      </div>
    </section>

    <!-- 1. Solution Summary -->
    <section class="section">
      <div class="summary-box">
        <div class="summary-row">
          <div class="summary-item">
            <div class="summary-label">適用產業</div>
            <div class="summary-value">會計師事務所 / 記帳士事務所</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">方案狀態</div>
            <div class="summary-value">Sandbox Demo（合成資料）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">部署模式</div>
            <div class="summary-value">每所獨立私有部署（非 SaaS）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">外部系統接軌</div>
            <div class="summary-value">正式會計軟體／ERP — 導入階段評估</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Highlights -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">1</span>
        為什麼事務所需要一套新的收件流程
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">💬</span>
          <div class="feature-title">LINE 翻拍、截圖、PDF 夾雜</div>
          <div class="feature-desc">客戶習慣用 LINE 傳發票，事務所逐張下載、整理、Key-in，旺季爆量時漏件與錯件的風險跟著上升。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🧾</span>
          <div class="feature-title">憑證格式雜，AI 不敢放手</div>
          <div class="feature-desc">電子發票 QR、傳統收據、POS 明細格式不一；直接讓 AI 自動入帳風險高，事務所找不到折衷的檢核流程。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔒</span>
          <div class="feature-title">集中雲端保存的疑慮</div>
          <div class="feature-desc">SaaS 集中保存客戶憑證，事務所對資料權威與稽核責任難以掌握；客戶資料外流疑慮成為導入最大阻力。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔄</span>
          <div class="feature-title">收件 → 檢核 → 覆核閉環</div>
          <div class="feature-desc">可驗證的 LINE 收件流程：AI 只產出候選，Pilot 期間全程人工覆核，每一筆都留下可稽核軌跡。</div>
        </div>
      </div>
    </section>

    <!-- 3. Flow Diagram -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">2</span>
        可驗證的收件 → 檢核 → 覆核閉環
      </div>
      <div class="flow-wrap">
        <div class="flow-diagram" role="img" aria-label="LINE 上傳發票、收件確認、辨識候選、LINE 內檢核、覆核核准與匯出的流程示意圖">
          <div class="flow-step">
            <div class="flow-icon">💬</div>
            <div class="flow-label">LINE 上傳</div>
            <div class="flow-sub">客戶上傳發票<br>即回覆收件確認</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">🔍</div>
            <div class="flow-label">辨識候選</div>
            <div class="flow-sub">QR／OCR 產出<br>可覆核候選</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">✏️</div>
            <div class="flow-label">LINE 內檢核</div>
            <div class="flow-sub">事務所檢核、<br>修正、確認</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">🛡️</div>
            <div class="flow-label">覆核核准</div>
            <div class="flow-sub">Pilot 全程人工<br>核准後才匯出</div>
          </div>
        </div>
        <div class="flow-caption">合成資料 Sandbox Demo 可完整展示此流程。未完成綁定的使用者，系統不下載原圖、不 OCR、不建立案件；正式憑證與稽核記錄留在事務所私有環境。操作畫面於 Demo 時提供。</div>
      </div>
    </section>

    <!-- 4. Boundary -->
    <section class="section">
      <div class="section-title"><span class="section-title-num">3</span>能力邊界</div>
      <div class="boundary-grid">
        <article class="boundary-card boundary-card--now"><h3>現可驗證（Sandbox Demo）</h3><ul><li>LINE 上傳 → 收件確認 → QR／OCR 辨識候選</li><li>LINE 內檢核修正 → 覆核 → 匯出預覽</li><li>全程稽核軌跡與唯讀 auditor 身分</li></ul></article>
        <article class="boundary-card boundary-card--poc"><h3>Pilot 可配置</h3><ul><li>1 家設計夥伴事務所；簽署 DPA 後才匯入真實資料</li><li>Pilot 強制 MFA（OIDC）、全程人工覆核核准</li><li>用途與保存政策確認後才正式使用</li></ul></article>
        <article class="boundary-card boundary-card--assessment"><h3>導入階段評估</h3><ul><li>正式會計軟體／ERP adapter</li><li>本地模型、備份還原演練與 SLA</li><li>自動化範圍與覆核政策於導入階段評估；正式覆核與匯出權限保留於事務所</li></ul></article>
      </div>
    </section>

    <!-- Target Audience -->
    <section class="section" id="target-audience">
      <div class="section-title">
        <span class="section-title-num">4</span>
        方案適合對象與導入前提
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">🏢</span>
          <div class="feature-title">會計師與記帳士事務所</div>
          <div class="feature-desc">客戶習慣以 LINE 傳遞發票，且希望正式帳務資料留在自己可控環境的事務所。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">📋</span>
          <div class="feature-title">需要可控流程的管理者</div>
          <div class="feature-desc">希望將收件、檢核、覆核變成可追蹤、可稽核工作流，並降低旺季漏件錯件風險。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🧪</span>
          <div class="feature-title">願意先驗證的事務所</div>
          <div class="feature-desc">願意先以合成資料驗證流程、簽署 DPA，並接受 Pilot 期間全程人工覆核核准。</div>
        </div>
      </div>
    </section>

    <!-- 5. Pricing + CTA -->
    <section class="section">
      <div class="cta-box">
        <div class="cta-title">導入方案（每所私有部署）</div>
        <div class="cta-desc"><strong>標準商用：首年 NT$360,000</strong>（一次性導入 NT$180,000＋年度授權 NT$150,000＋年度基本維護 NT$30,000；未稅）。另有首批標準導入版（首年 17.2–26.4 萬：限標準環境＋固定名額＋無重大客製）與多站治理版（首年 51.4 萬起：需求盤點後報價）。主機、OCR、LINE、儲存與第三方介接另計；實際導入依事務所規模、憑證量與驗收內容確認。</div>
        <div class="cta-actions" id="demo-actions">
          <a href="../../contact.html?request_type=ledger_assist_assessment&amp;utm_source=site&amp;utm_medium=ledger_assist&amp;utm_campaign=ledger_assist_v2&amp;utm_content=footer_cta" class="btn btn-primary" id="btn-demo-request">預約私有工作流程評估</a>
        </div>
        <div class="consent-text">點擊提交表單即表示您已詳閱並同意<a href="../../privacy.html">《個人資料保護與隱私權政策告知書》</a>。本系統提供發票文字辨識與帳務初分類輔助；實際成效依憑證品質、既有流程及驗收數據評估，最終憑證核對、帳務審核及稅務申報責任由專業人員承擔。</div>
      </div>
    </section>
"""
# ── AI Allocation OS ──
aos_container = """    <header class="page-header">
      <a href="../index.html" class="back-link">← 返回體驗區總覽</a>
      <div class="page-header-right">
        <div class="status-badge">
          <span class="status-dot"></span>
          Consulting Offer
        </div>
        <span class="logo-mark">鳳凰 AI</span>
      </div>
    </header>

    <section class="hero">
      <div class="hero-glow"></div>
      <div class="hero-content">
        <div class="hero-tag">AI Investment Decision · Consulting Sprint</div>
        <h1 class="hero-title">AI Allocation OS 企業 AI 投資決策工作台</h1>
        <p class="hero-desc">AI 提案很多、預算有限——該投哪個、該修哪個、該延後哪個？我們以 Capital Decision Sprint 顧問服務，用版本化規則、可追溯證據與預先定義的風險 Gate，把決策過程收成可稽核的決策包。這是顧問服務，不是賣軟體：把「怎麼決定」變成可檢討、可重現的流程。</p>
        <div class="hero-actions" id="hero-actions">
          <a href="../../contact.html?request_type=capital_sprint_info&amp;utm_source=site&amp;utm_medium=ai_allocation_os&amp;utm_campaign=capital_sprint&amp;utm_content=hero" class="btn btn-primary" id="btn-demo-request-2">預約 30–45 分鐘說明</a>
        </div>
      </div>
    </section>

    <!-- 1. Solution Summary -->
    <section class="section">
      <div class="summary-box">
        <div class="summary-row">
          <div class="summary-item">
            <div class="summary-label">適用產業</div>
            <div class="summary-value">零售／電商／B2C 服務業（客服營運）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">方案狀態</div>
            <div class="summary-value">Consulting Offer｜開放預約</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">交付模式</div>
            <div class="summary-value">顧問 Sprint（非軟體授權）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">服務時程</div>
            <div class="summary-value">kickoff 後 10 個工作日內完成</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Highlights -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">1</span>
        AI 投資決策為何難以檢討
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">📊</span>
          <div class="feature-title">提案多、標準不一</div>
          <div class="feature-desc">AI 提案逐年增加，各提案用不同標準評估；Fund、Repair、Defer、Reject 常靠會議感覺，事後難以回溯理由。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🧩</span>
          <div class="feature-title">理由沒版本、沒證據</div>
          <div class="feature-desc">決策理由沒有版本化、沒有證據連結；幾個月後回頭看，已無法重現「當時為什麼這樣決定」。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">⚖️</span>
          <div class="feature-title">評分容易受立場影響</div>
          <div class="feature-desc">提案方、供應商與決策者各有立場；缺少中立、且可留下紀錄的決策流程。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🎯</span>
          <div class="feature-title">決策後缺乏追蹤</div>
          <div class="feature-desc">沒有 baseline 與 30／60／90 天回報機制，投入之後無法驗證當初假設是否成立。</div>
        </div>
      </div>
    </section>

    <!-- 3. Flow Diagram -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">2</span>
        Capital Decision Sprint 內容
      </div>
      <div class="flow-wrap">
        <div class="flow-diagram" role="img" aria-label="候選篩選、深度 Underwriting、三軸決策、風險 Gate 與 Committee Pack 交付的流程示意圖">
          <div class="flow-step">
            <div class="flow-icon">🔍</div>
            <div class="flow-label">候選篩選</div>
            <div class="flow-sub">最多 5 個<br>客服分類候選</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">📋</div>
            <div class="flow-label">Underwriting</div>
            <div class="flow-sub">3 個深度評估<br>附證據理由</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">🧭</div>
            <div class="flow-label">三軸決策</div>
            <div class="flow-sub">Fund／Repair<br>／Defer／Reject</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">🛡️</div>
            <div class="flow-label">風險 Gate</div>
            <div class="flow-sub">Funding／Repair<br>／Reassessment</div>
          </div>
        </div>
        <div class="flow-caption">決策快照 T0／T1／T2 全程留痕；LLM 只負責抽取、解釋與草擬，不直接決定分數。最終決策權與責任由客戶承擔。</div>
      </div>
    </section>

    <!-- 4. Boundary -->
    <section class="section">
      <div class="section-title"><span class="section-title-num">3</span>能力邊界</div>
      <div class="boundary-grid">
        <article class="boundary-card boundary-card--now"><h3>本服務範圍</h3><ul><li>決策支援與分析（顧問 Sprint）</li><li>候選篩選、Underwriting、三軸決策與風險 Gate</li><li>Committee Pack、Decision Record 與 action log</li></ul></article>
        <article class="boundary-card boundary-card--poc"><h3>不包含</h3><ul><li>實際 AI 系統開發、PoC 或導入執行（可另行報價）</li><li>法律、財務、稅務、合規或證券投資專業意見</li><li>保證 ROI、投資成功或特定決策結果</li></ul></article>
        <article class="boundary-card boundary-card--assessment"><h3>中立性與資料最小化</h3><ul><li>Sprint 費用不因決策結果改變；後續承接與決策紀錄分離</li><li>僅收聚合流程量、KPI baseline、欄位字典與 metadata</li><li>樣本 50–100 筆去識別化且須先核准；benchmark 獨立 opt-in</li></ul></article>
      </div>
    </section>

    <!-- Target Audience -->
    <section class="section" id="target-audience">
      <div class="section-title">
        <span class="section-title-num">4</span>
        方案適合對象與導入前提
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">🛒</span>
          <div class="feature-title">零售／電商／B2C 服務業</div>
          <div class="feature-desc">客服案件分類／分流流程，每月案件量約 1,000 件以上，且 30–60 天內可建立或量測 baseline。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">📈</span>
          <div class="feature-title">可量測 KPI 的營運團隊</div>
          <div class="feature-desc">至少一項可量測指標（平均處理時間、首次回應時間、轉人工率），量不出就不做。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">👥</span>
          <div class="feature-title">具名決策者與 process owner</div>
          <div class="feature-desc">願意提供可驗證的歷史聚合資料；受高度監管產業需另備具名 compliance／risk sponsor。</div>
        </div>
      </div>
    </section>

    <!-- 5. Investment -->
    <section class="section">
      <div class="cta-box">
        <div class="cta-title">專案投資金額</div>
        <div class="cta-desc"><strong>Capital Decision Sprint：NT$280,000 起（含稅）</strong>。實際投資金額依企業規模、候選流程數量與資料準備狀況進行增減，於正式提案中確認。訂金 NT$80,000、尾款 NT$200,000（會議結束後 7 天內）。</div>
        <div class="cta-actions" id="demo-actions">
          <a href="../../contact.html?request_type=capital_sprint_info&amp;utm_source=site&amp;utm_medium=ai_allocation_os&amp;utm_campaign=capital_sprint&amp;utm_content=footer_cta" class="btn btn-primary" id="btn-demo-request">預約 30–45 分鐘說明</a>
        </div>
        <div class="consent-text">點擊提交表單即表示您已詳閱並同意<a href="../../privacy.html">《個人資料保護與隱私權政策告知書》</a></div>
      </div>
    </section>
"""
# ── AI 律師工作台（SYS-09，2026-08-14 納入生成器）──
sys09_container = """    <header class="page-header">
      <a href="../index.html" class="back-link">← 返回體驗區總覽</a>
      <div class="page-header-right">
        <div class="status-badge">
          <span class="status-dot"></span>
          Sandbox Demo
        </div>
        <span class="logo-mark">鳳凰 AI</span>
      </div>
    </header>

    <section class="hero">
      <div class="hero-glow"></div>
      <div class="hero-content">
        <div class="hero-tag">Legal Practice · Matter Workflow</div>
        <h1 class="hero-title">AI 律師工作台</h1>
        <p class="hero-desc">以「案件（Matter）→ 程序（Proceeding）→ 狀態（State）」狀態機管理民事案件，搭配紅線／黃線法條期限引擎、AI 草稿與雙人覆核。每所律師事務所獨立私有部署；未取得當事人書面同意前，系統預設使用 synthetic／本地配置，不對外送出案件資料。正式導入依事務所權限、案件類型與驗收為準。</p>
        <div class="hero-actions" id="hero-actions">
          <a href="../../contact.html?request_type=ai_lawyer_assessment&amp;utm_source=site&amp;utm_medium=ai_lawyer_workbench&amp;utm_campaign=ai_lawyer_v2&amp;utm_content=hero" class="btn btn-primary" id="btn-demo-request-2">預約私有工作流程評估</a>
        </div>
      </div>
    </section>

    <!-- 1. Solution Summary -->
    <section class="section">
      <div class="summary-box">
        <div class="summary-row">
          <div class="summary-item">
            <div class="summary-label">適用產業</div>
            <div class="summary-value">律師事務所（民事案件管理）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">方案狀態</div>
            <div class="summary-value">Sandbox Demo（合成資料）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">部署模式</div>
            <div class="summary-value">每所獨立私有部署（非 SaaS）</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">LLM 設定</div>
            <div class="summary-value">synthetic 預設／本地／外部需當事人書面同意</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Highlights -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">1</span>
        律師事務所的案件與期限管理為何需要數位化
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">🗓️</span>
          <div class="feature-title">期限分散在行事曆與紙本</div>
          <div class="feature-desc">民事案件的法院法定期間分散在行事曆、Excel 與紙本卷宗；律師同時處理多案時，漏期風險與確認成本同步上升。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">✍️</span>
          <div class="feature-title">書狀草稿反覆修改</div>
          <div class="feature-desc">AI 草稿可依案件狀態與引用來源產生初稿，仍需律師覆核、補強與最終署名；每次產出皆經律師確認後才使用。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔒</span>
          <div class="feature-title">律師保密與個資敏感</div>
          <div class="feature-desc">案件涉及律師業務秘密與當事人個資；獨立私有部署、權限隔離與雙人覆核，是導入時的基本要求。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔄</span>
          <div class="feature-title">狀態與覆核可追蹤</div>
          <div class="feature-desc">Matter→Proceeding→State 狀態機、倫理牆與稽核軌跡，讓每個案件從開案到結案的關鍵動作都有紀錄。</div>
        </div>
      </div>
    </section>

    <!-- 3. Flow Diagram -->
    <section class="section">
      <div class="section-title">
        <span class="section-title-num">2</span>
        案件狀態機與雙軌期限引擎
      </div>
      <div class="flow-wrap">
        <div class="flow-diagram" role="img" aria-label="開案、程序狀態推進、紅線黃線期限計算、AI 草稿與雙人覆核、匯出的流程示意圖">
          <div class="flow-step">
            <div class="flow-icon">📂</div>
            <div class="flow-label">開案</div>
            <div class="flow-sub">衝突檢核<br>建立 Matter</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">⚙️</div>
            <div class="flow-label">狀態推進</div>
            <div class="flow-sub">Proceeding<br>→ State</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">⏰</div>
            <div class="flow-label">期限引擎</div>
            <div class="flow-sub">紅線／黃線<br>法條期限</div>
          </div>
          <div class="flow-arrow">›</div>
          <div class="flow-step">
            <div class="flow-icon">🛡️</div>
            <div class="flow-label">雙人覆核</div>
            <div class="flow-sub">書狀／意見<br>雙簽後匯出</div>
          </div>
        </div>
        <div class="flow-caption">本系統提供期限紀錄與提醒之輔助管理功能，律師及事務所仍負有獨立核對法院法定期間與送達證書之最終責任。AI 草稿僅為輔助，最終法律判斷與署名由律師負責。</div>
      </div>
    </section>

    <!-- 4. Boundary -->
    <section class="section">
      <div class="section-title"><span class="section-title-num">3</span>能力邊界</div>
      <div class="boundary-grid">
        <article class="boundary-card boundary-card--now"><h3>現可驗證（Sandbox Demo）</h3><ul><li>Matter→Proceeding→State 狀態機與 ACL 權限</li><li>紅線／黃線法條期限計算與提醒</li><li>AI 草稿（synthetic 或本地）＋citation 驗證＋雙人覆核</li><li>LOCKED 匯出與稽核軌跡</li></ul></article>
        <article class="boundary-card boundary-card--poc"><h3>導入前提（受控試點）</h3><ul><li>簽署 DPA 與法顧附錄 A（當事人知情同意）後，才可啟用外部 LLM 外送</li><li>未取得同意前強制 synthetic／本地配置，不對外送出案件資料</li><li>OIDC／MFA 為選配、逐案設計，不預設為完整落地</li></ul></article>
        <article class="boundary-card boundary-card--assessment"><h3>導入階段評估</h3><ul><li>事務所流程、案件類型與權限政策盤點</li><li>期限規則對齊事務所慣例與法院實務</li><li>備份還原演練、監控告警與 SLA 於導入階段確認</li></ul></article>
      </div>
    </section>

    <!-- Target Audience -->
    <section class="section" id="target-audience">
      <div class="section-title">
        <span class="section-title-num">4</span>
        方案適合對象與導入前提
      </div>
      <div class="feature-grid">
        <div class="feature-card">
          <span class="feature-icon">🏛️</span>
          <div class="feature-title">重視期限管理的事務所</div>
          <div class="feature-desc">希望將案件期限、狀態與覆核變成可追蹤、可稽核流程，降低漏期風險。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🔐</span>
          <div class="feature-title">重視保密與資料控制者</div>
          <div class="feature-desc">希望案件資料留在自己可控的私有環境，不接受集中式 SaaS 保存律師業務秘密。</div>
        </div>
        <div class="feature-card">
          <span class="feature-icon">🧪</span>
          <div class="feature-title">願意先驗證者</div>
          <div class="feature-desc">願意先以合成資料驗證流程、簽署 DPA，並在受控範圍內確認 AI 輔助與雙人覆核政策。</div>
        </div>
      </div>
    </section>

    <!-- 5. Pricing + CTA -->
    <section class="section">
      <div class="cta-box">
        <div class="cta-title">導入方案（每所私有部署）</div>
        <div class="cta-desc"><strong>標準商用：首年 NT$840,000</strong>（一次性導入 NT$600,000＋年度授權/法規更新 NT$240,000；未稅）。另有小型所方案（首年 54 萬起：導入 36 萬＋年度 18 萬）與中型所方案（首年 168 萬起：導入 120 萬＋年度 48 萬）。主機、外部 LLM 用量、OIDC 整合與客製介接另計；實際導入依事務所規模、案件類型與驗收內容確認。</div>
        <div class="cta-actions" id="demo-actions">
          <a href="../../contact.html?request_type=ai_lawyer_assessment&amp;utm_source=site&amp;utm_medium=ai_lawyer_workbench&amp;utm_campaign=ai_lawyer_v2&amp;utm_content=footer_cta" class="btn btn-primary" id="btn-demo-request">預約私有工作流程評估</a>
        </div>
        <div class="consent-text">點擊提交表單即表示您已詳閱並同意<a href="../../privacy.html">《個人資料保護與隱私權政策告知書》</a>。本系統提供期限紀錄與提醒之輔助管理功能，律師及事務所仍負有獨立核對法院法定期間與送達證書之最終責任；AI 產出須經律師覆核，最終法律判斷與署名由律師負責。</div>
      </div>
    </section>
"""
def main():
    parser = argparse.ArgumentParser(description="Build solution pages")
    parser.add_argument("--target", action="append", choices=["ledger-assist", "ai-allocation-os", "ai-lawyer-workbench"],
                        help="只生成指定目標（可重複）；未指定＝全生成")
    args = parser.parse_args()
    targets = args.target or ["ledger-assist", "ai-allocation-os", "ai-lawyer-workbench"]
    if "ledger-assist" in targets:
        build("ledger-assist", ledger_container, "ledger_assist", "Ledger-Assist 發票收件與檢核系統", "Accounting · LINE Workflow")
    if "ai-allocation-os" in targets:
        build("ai-allocation-os", aos_container, "ai_allocation_os", "AI Allocation OS 企業 AI 投資決策工作台", "AI Investment Decision · Consulting Sprint")
    if "ai-lawyer-workbench" in targets:
        build("ai-lawyer-workbench", sys09_container, "ai_lawyer_workbench", "AI 律師工作台", "Legal Practice · Matter Workflow")
    print("DONE")

if __name__ == "__main__":
    main()
