# -*- coding: utf-8 -*-
"""Generate /experience/stories/ hub, season, and episode pages. YouTube embeds only; no mp4."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experience" / "stories"
SITE = "https://03king.com"
CHANNEL = "https://www.youtube.com/channel/UCB8ylkjHsaqcYqIgnyU9Y-w"
S1_PLAYLIST = "https://www.youtube.com/playlist?list=PLSwU1EWDBWxw"
OG = "https://03king.com/assets/og-image.png?v=20260810"
GTM = "GTM-NB4699JG"

SEASONS = [
    {
        "id": "s1",
        "num": 1,
        "title": "誰在搞鬼？",
        "subtitle": "第一季《律所裡的那隻手》",
        "track": "law",
        "track_label": "律師期限與覆核",
        "product_name": "AI 律師工作台",
        "product_href": "../ai-lawyer-workbench/",
        "playlist": S1_PLAYLIST,
        "blurb": "期限、卷宗、權限。有人在所裡動手腳。",
        "status": "youtube",
        "episodes": [
            {
                "n": 1,
                "slug": "e01",
                "title": "期限危機",
                "youtube_id": "NwJ1QjsJBpI",
                "scene": "期限要到了，卷宗對不上。",
                "stuck": "一個人開所，期限與版本全憑記憶。",
                "system": "期限依據集中紀錄與提前提醒；草稿與覆核留痕。",
                "not_replace": "判斷仍在律師手上。",
            },
            {
                "n": 2,
                "slug": "e02",
                "title": "卷宗不見了",
                "youtube_id": "VUEjtFJHBfU",
                "scene": "要交接的卷宗，桌上沒有、系統對不到。",
                "stuck": "找不到上一手是誰、哪一版才算數。",
                "system": "收件與版本集中紀錄，覆核留得住。",
                "not_replace": "不取代律師對卷證的判斷。",
            },
            {
                "n": 3,
                "slug": "e03",
                "title": "客戶要撤案",
                "youtube_id": "-PEXwnFZQDM",
                "scene": "客戶要撤，期限與責任卻還掛在所裡。",
                "stuck": "口頭答應、紙本對不上，誰都說不清楚。",
                "system": "案件狀態與覆核紀錄可追溯。",
                "not_replace": "撤案與否仍是律師與當事人決定。",
            },
            {
                "n": 4,
                "slug": "e04",
                "title": "名子寫錯",
                "youtube_id": "h1R9GLlbFII",
                "scene": "書狀上的名字不對。",
                "stuck": "是手滑，還是用了錯的版本。",
                "system": "草稿先起、雙人覆核留痕，再送出。",
                "not_replace": "署名與對外文書仍是律師責任。",
            },
            {
                "n": 5,
                "slug": "e05",
                "title": "卷宗打不開",
                "youtube_id": "NVC3aYvQneE",
                "scene": "要開的卷宗打不開，缺頁對不上。",
                "stuck": "昨晚誰開過、哪兩頁不見了，沒有紀錄。",
                "system": "操作與版本集中紀錄，方便核對。",
                "not_replace": "不取代律師對證據完整性的判斷。",
            },
            {
                "n": 6,
                "slug": "e06",
                "title": "發票重覆報",
                "youtube_id": "lD0Ht-Lk4Ng",
                "scene": "同一筆費用，報了兩次。",
                "stuck": "重複看不見，對帳只能靠人海。",
                "system": "重複與缺件集中標出，等人確認。",
                "not_replace": "核銷與否仍是事務所決定。",
            },
            {
                "n": 7,
                "slug": "e07",
                "title": "申報人消失",
                "youtube_id": "R9_07xFQCeI",
                "scene": "申報人從紀錄裡不見了。",
                "stuck": "外部壓力上來，內部對不到人。",
                "system": "狀態與依據集中紀錄，方便追查。",
                "not_replace": "對外法律意見仍須律師覆核。",
            },
            {
                "n": 8,
                "slug": "e08",
                "title": "你查我權限",
                "youtube_id": "ltXNyi8ewO0",
                "scene": "要查資料，被擋在權限外。",
                "stuck": "該看的人看不到，不該動的人卻動過。",
                "system": "權限與覆核分開，敏感動作留痕。",
                "not_replace": "授權範圍由事務所自己定。",
            },
            {
                "n": 9,
                "slug": "e09",
                "title": "契約書找不到",
                "youtube_id": "obhss7AG2W0",
                "scene": "要的契約，資料夾裡沒有。",
                "stuck": "新人找不到、舊人憑記憶。",
                "system": "文件與版本集中，引用對得到出處。",
                "not_replace": "契約效力仍由律師判斷。",
            },
            {
                "n": 10,
                "slug": "e10",
                "title": "內鬼在刪資料",
                "youtube_id": "nKn5rBBo81s",
                "scene": "有人在刪所裡的資料。",
                "stuck": "刪了才發現，來不及對。",
                "system": "敏感操作留痕，覆核看得到。",
                "not_replace": "人事與法律責任不交給系統。",
            },
        ],
    },
    {
        "id": "s2",
        "num": 2,
        "title": "決策的價格",
        "subtitle": "第二季",
        "track": "fac",
        "track_label": "工廠帳實與簽收",
        "product_name": "製造現場協助",
        "product_href": "../index.html",
        "playlist": "",
        "blurb": "帳上說貨到了，架上是空的。",
        "status": "upcoming",
        "episodes": [],
    },
    {
        "id": "s3",
        "num": 3,
        "title": "帳上的神祕通道",
        "subtitle": "第三季",
        "track": "acc",
        "track_label": "會計憑證與月結",
        "product_name": "AI 會計工作台",
        "product_href": "../ledger-assist/",
        "playlist": "",
        "blurb": "證據鏈伸進事務所。",
        "status": "approved_not_youtube",
        "episodes": [
            {
                "n": 1,
                "slug": "e01",
                "title": "漂亮的罰單",
                "youtube_id": "",
                "scene": "罰單在帳上很漂亮，發票卻在所裡流動。",
                "stuck": "月結缺件看不見，覆核只靠口頭。",
                "system": "LINE 上傳與人覆核，證據留在事務所自己的環境。",
                "not_replace": "不取代會計師。",
            },
            {
                "n": 2,
                "slug": "e02",
                "title": "第二張發票",
                "youtube_id": "",
                "scene": "第二張發票對不上第一張故事。",
                "stuck": "重複與缺件要等人把兩張攤開才看見。",
                "system": "憑證收件、重複與缺件集中標出，等人確認。",
                "not_replace": "不取代會計師。",
            },
        ],
    },
]

# Fix E10 id typo if I mistyped — verified id is nKn5rRBo81s
SEASONS[0]["episodes"][9]["youtube_id"] = "nKn5rRBo81s"

DISCLAIMER = "合成劇情、顧問課作品集。不是客戶實績，不保證成效。不取代律師／會計判斷。"


def css() -> str:
    return """
    :root {
      --phoenix-dark: #0B0B16; --phoenix-mid: #121226; --phoenix-accent: #E94560;
      --phoenix-teal: #00F2FE; --phoenix-gold: #F5A623; --white: #FFFFFF;
      --gray-300: #DDE2E5; --gray-400: #A5B1B8; --gray-600: #5A6A75;
      --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
      --font-body: 'Inter', 'Noto Sans TC', sans-serif;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { background: var(--phoenix-dark); color: var(--white); font-family: var(--font-body); line-height: 1.6; }
    body { background: radial-gradient(circle at 50% -20%, #201a35 0%, #0b0b16 60%); min-height: 100vh; display: flex; flex-direction: column; }
    a { color: inherit; text-decoration: none; }
    .container { width: 100%; max-width: 1120px; margin: 0 auto; padding: 0 24px; }
    .page-header { padding: 20px 0; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .back-link { color: var(--gray-400); font-size: 14px; }
    .back-link:hover { color: var(--white); }
    .logo-mark { color: var(--phoenix-gold); font-family: var(--font-display); letter-spacing: .12em; font-size: 12px; }
    .kicker { color: var(--phoenix-gold); font-size: 12px; letter-spacing: .16em; margin-bottom: 8px; }
    h1 { font-family: var(--font-display); font-size: clamp(28px, 4vw, 44px); line-height: 1.2; font-weight: 600; margin: 0 0 12px; }
    h2 { font-size: 20px; margin: 0 0 10px; }
    p { color: var(--gray-400); }
    .tracks { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 24px; }
    .tracks a, .tracks button, .btn {
      background: transparent; color: var(--white); border: 1px solid rgba(255,255,255,.12);
      padding: 8px 14px; cursor: pointer; font: inherit; display: inline-block;
    }
    .tracks a.is-on, .tracks button.is-on { border-color: var(--phoenix-accent); color: var(--phoenix-accent); }
    .btn-primary { border-color: var(--phoenix-accent); margin-right: 10px; margin-top: 12px; }
    .btn-ghost { margin-top: 12px; }
    .row { display: grid; grid-template-columns: 280px 1fr; gap: 28px; align-items: start; }
    @media (max-width: 840px) { .row { grid-template-columns: 1fr; } }
    .phone { width: 100%; max-width: 280px; aspect-ratio: 9/16; background: #000; border: 1px solid rgba(255,255,255,.08); overflow: hidden; position: relative; }
    .phone iframe { width: 100%; height: 100%; border: 0; }
    .poster { position: absolute; inset: 0; display: flex; align-items: flex-end; padding: 16px; font-size: 14px; color: var(--gray-300); background: linear-gradient(180deg,#1a1a2e,#000); }
    .four { color: var(--white); font-size: 15px; margin: 0 0 8px; }
    .four span { color: var(--phoenix-gold); margin-right: 8px; }
    .season { display: grid; grid-template-columns: 72px 1fr 160px; gap: 10px; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,.08); font-size: 14px; }
    .season span { color: var(--gray-400); }
    .ok { color: var(--phoenix-teal) !important; }
    .wait { color: var(--gray-600) !important; }
    .note { font-size: 13px; color: var(--gray-600); margin: 32px 0 48px; }
    .footer { margin-top: auto; padding: 28px 0; border-top: 1px solid rgba(255,255,255,.04); text-align: center; color: var(--gray-600); font-size: 12px; }
    .footer a { color: var(--gray-400); margin: 0 8px; }
    """


def head(title: str, desc: str, canonical: str, extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="{canonical}">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{OG}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG}">
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{GTM}');</script>
  {extra}
  <style>{css()}</style>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
"""


def foot(root_prefix: str) -> str:
    return f"""
  <footer class="footer">
    <div class="container">
      <a href="{root_prefix}index.html">首頁</a>
      <a href="{root_prefix}experience/index.html">體驗區</a>
      <a href="{root_prefix}privacy.html">隱私權政策</a>
      <p style="margin-top:12px">© 2026 鳳凰 AI 顧問團隊。{DISCLAIMER}</p>
    </div>
  </footer>
</body>
</html>
"""


def embed(vid: str, title: str) -> str:
    if not vid:
        return '<div class="phone"><div class="poster">這一集尚未在 YouTube 公開播放。</div></div>'
    src = f"https://www.youtube.com/embed/{vid}"
    return f'<div class="phone"><iframe title="{title}" src="{src}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'


def four(ep: dict) -> str:
    return f"""
          <p class="four"><span>現場</span>{ep['scene']}</p>
          <p class="four"><span>卡住</span>{ep['stuck']}</p>
          <p class="four"><span>系統</span>{ep['system']}</p>
          <p class="four"><span>不取代</span>{ep['not_replace']}</p>
"""


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html.replace("\n", "\r\n"), encoding="utf-8")
    print("wrote", path, path.stat().st_size)


def build_hub() -> None:
    s1e1 = SEASONS[0]["episodes"][0]
    jsonld = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"TVSeries","name":"鳳凰 AI 短劇作品集","inLanguage":"zh-Hant","publisher":{"@type":"Organization","name":"鳳凰 AI"}}</script>"""
    html = head(
        "鳳凰 AI 短劇作品集｜用故事看懂事務所怎麼做事",
        "律師期限、會計憑證、工廠帳實三條線。合成作品集，不是客戶實績。",
        f"{SITE}/experience/stories/",
        jsonld,
    )
    html += f"""
  <div class="container">
    <header class="page-header">
      <a class="back-link" href="../index.html">← 返回體驗區</a>
      <span class="logo-mark">鳳凰 AI</span>
    </header>
    <p class="kicker">鳳凰 AI 短劇作品集</p>
    <h1>用連載故事，看懂事務所裡真正卡住的事。</h1>
    <p>正片在 YouTube。這裡給顧問看「這一集在解什麼」，再帶進工作台。{DISCLAIMER}</p>
    <div class="tracks">
      <a class="is-on" href="./s1/">律師期限與覆核</a>
      <a href="./s3/">會計憑證與月結</a>
      <a href="./s2/">工廠帳實與簽收</a>
    </div>
    <div class="row">
      {embed(s1e1['youtube_id'], s1e1['title'])}
      <div>
        <p class="kicker">現在可看 · 第1季第1集</p>
        <h2>{s1e1['title']}</h2>
        {four(s1e1)}
        <a class="btn btn-primary" href="../ai-lawyer-workbench/">看 AI 律師工作台展示</a>
        <a class="btn btn-ghost" href="{S1_PLAYLIST}" rel="noopener">在 YouTube 看完整一季</a>
        <p style="margin-top:14px;font-size:13px"><a href="./s1/e01/" style="color:var(--phoenix-teal)">打開這一集的說明頁 →</a></p>
      </div>
    </div>
    <h2 style="margin-top:40px">連載</h2>
    <div class="season"><b>S1</b><span>《誰在搞鬼？》／《律所裡的那隻手》 · AI 律師工作台</span><span class="ok"><a href="./s1/">YouTube 已上 E1–E10</a></span></div>
    <div class="season"><b>S2</b><span>《決策的價格》 · 工廠帳實</span><span class="wait">籌備中</span></div>
    <div class="season"><b>S3</b><span>《帳上的神祕通道》 · AI 會計工作台</span><span class="wait"><a href="./s3/">目錄已開，正片尚未上 YouTube</a></span></div>
    <div class="season"><b>S4+</b><span>下一季連載位</span><span class="wait">有新痛點再開季</span></div>
    <p class="note">只連短劇播放清單，不連整個頻道。頻道另有課程與評論，避免顧問點進去迷路。</p>
  </div>
"""
    html += foot("../../")
    write(OUT / "index.html", html)


def build_season(season: dict) -> None:
    sid = season["id"]
    jsonld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TVSeason","name":"{season["title"]} {season["subtitle"]}","seasonNumber":{season["num"]},"partOfSeries":{{"@type":"TVSeries","name":"鳳凰 AI 短劇作品集"}}}}</script>'
    rows = []
    if not season["episodes"]:
        rows.append('<div class="season"><b>—</b><span>本季集數尚未公開。</span><span class="wait">未公開</span></div>')
    for ep in season["episodes"]:
        href = f'./{ep["slug"]}/'
        if ep.get("youtube_id"):
            st = f'<a class="ok" href="{href}">可看</a>'
        else:
            st = f'<a class="wait" href="{href}">說明頁 · 未在 YouTube 公開</a>'
        rows.append(f'<div class="season"><b>E{ep["n"]}</b><span><a href="{href}">{ep["title"]}</a></span><span>{st}</span></div>')
    pl = ""
    if season.get("playlist"):
        pl = f'<a class="btn btn-ghost" href="{season["playlist"]}" rel="noopener">在 YouTube 連續播放</a>'
    html = head(
        f'{season["title"]}{season["subtitle"]}｜鳳凰 AI 短劇',
        f'{season["blurb"]} {DISCLAIMER}',
        f"{SITE}/experience/stories/{sid}/",
        jsonld,
    )
    html += f"""
  <div class="container">
    <header class="page-header">
      <a class="back-link" href="../">← 返回作品集總館</a>
      <span class="logo-mark">鳳凰 AI</span>
    </header>
    <p class="kicker">第 {season["num"]} 季 · {season["track_label"]}</p>
    <h1>《{season["title"]}》<br>{season["subtitle"]}</h1>
    <p>{season["blurb"]} {DISCLAIMER}</p>
    {pl}
    <div style="margin-top:28px">{''.join(rows)}</div>
    <p style="margin-top:24px"><a class="btn btn-primary" href="{season["product_href"]}">看{season["product_name"]}</a></p>
  </div>
"""
    html += foot("../../../")
    write(OUT / sid / "index.html", html)


def build_episode(season: dict, ep: dict, prev_ep: dict | None, next_ep: dict | None) -> None:
    sid = season["id"]
    title = f'{ep["title"]}｜第{season["num"]}季《{season["title"]}》｜{season["product_name"]}｜鳳凰 AI'
    desc = f'{ep["scene"]}{ep["stuck"]}{ep["system"]}{ep["not_replace"]} {DISCLAIMER}'
    canon = f"{SITE}/experience/stories/{sid}/{ep['slug']}/"
    extra = ""
    if ep.get("youtube_id"):
        extra = "<script type=\"application/ld+json\">" + json.dumps({
            "@context": "https://schema.org",
            "@type": "TVEpisode",
            "name": ep["title"],
            "episodeNumber": ep["n"],
            "partOfSeason": {"@type": "TVSeason", "seasonNumber": season["num"]},
            "partOfSeries": {"@type": "TVSeries", "name": "鳳凰 AI 短劇作品集"},
            "embedUrl": f"https://www.youtube.com/embed/{ep['youtube_id']}",
            "sameAs": f"https://www.youtube.com/shorts/{ep['youtube_id']}",
        }, ensure_ascii=False) + "</script>"
    nav = []
    if prev_ep:
        nav.append(f'<a href="../{prev_ep["slug"]}/">上一集《{prev_ep["title"]}》</a>')
    else:
        nav.append("上一集 —")
    if next_ep:
        nav.append(f'<a href="../{next_ep["slug"]}/">下一集《{next_ep["title"]}》</a>')
    else:
        nav.append("下一集 —")
    yt_link = ""
    if ep.get("youtube_id"):
        yt_link = f'<a class="btn btn-ghost" href="https://www.youtube.com/shorts/{ep["youtube_id"]}" rel="noopener">在 YouTube 打開</a>'
    prod = season["product_href"]
    if prod.startswith("../"):
        prod = "../../../" + prod[3:]  # season ../x → episode ../../../x
    html = head(title, desc, canon, extra)
    html += f"""
  <div class="container">
    <header class="page-header">
      <a class="back-link" href="../">← 返回第{season["num"]}季</a>
      <span class="logo-mark">鳳凰 AI</span>
    </header>
    <p class="kicker">S{season["num"]}E{ep["n"]} · {season["product_name"]}</p>
    <h1>{ep["title"]}</h1>
    <div class="row">
      {embed(ep.get("youtube_id") or "", ep["title"])}
      <div>
        <h2>這一集在解什麼</h2>
        {four(ep)}
        <a class="btn btn-primary" href="{prod}">看 {season["product_name"]}</a>
        {yt_link}
        <p style="margin-top:18px;font-size:13px;color:var(--gray-400)">{'　'.join(nav)}</p>
      </div>
    </div>
    <p class="note">{DISCLAIMER}</p>
  </div>
"""
    html += foot("../../../../")
    write(OUT / sid / ep["slug"] / "index.html", html)


def main() -> None:
    build_hub()
    for season in SEASONS:
        build_season(season)
        eps = season["episodes"]
        for i, ep in enumerate(eps):
            prev_ep = eps[i - 1] if i else None
            next_ep = eps[i + 1] if i + 1 < len(eps) else None
            build_episode(season, ep, prev_ep, next_ep)
    print("DONE")


if __name__ == "__main__":
    main()
