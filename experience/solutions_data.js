/* Phoenix AI system registry.
 * Homepage featured cards and the full systems catalog read from this file.
 * Keep public copy de-identified and free of internal implementation details.
 */

window.EXPERIENCE_SOLUTIONS = [
  {
    id: "central_kitchen_operations_guard",
    slug: "central-kitchen-ai-agent",
    title: "中央廚房營運防護台",
    short_title: "營運防護台",
    subtitle: "把履約事件、門市開單與總部例外治理收成可驗證閉環",
    status: "Pilot-ready Sandbox",
    maturity: "Pilot Ready",
    access_type: "公開預覽／預約 Demo",
    featured: true,
    featured_order: 1,
    category: ["營運治理", "餐飲"],
    industries: ["餐飲連鎖", "中央廚房", "零售連鎖"],
    page_variant: "operations",
    showcase_type: "dual-workbench",
    demo_duration: "15 分鐘",
    highlights: [
      "履約訊號進入門市今日必做，顧客不必登入系統",
      "結構化動作卡經規則評分；Pro 可自決或送總部審核",
      "核准後產出對客文案與 ERP／POS 沙盒預覽"
    ],
    sections: ["event-flow", "dual-workbench", "tier-ladder", "boundaries", "pilot-cta"],
    compliance_note: "Sandbox Demo；對客通知與 ERP／POS payload 僅為模擬預覽，不寫入正式系統。",
    cta_text: "查看營運防護台",
    cta_href: "./experience/central-kitchen-ai-agent/index.html",
    catalog_cta_href: "./central-kitchen-ai-agent/index.html",
    pilot_program_text: "預約 15 分鐘 Demo",
    pilot_program_href: "./contact.html?request_type=central_kitchen_demo&utm_source=site&utm_medium=central_kitchen&utm_campaign=central_kitchen_demo&utm_content=flagship",
    catalog_pilot_program_href: "../contact.html?request_type=central_kitchen_demo&utm_source=site&utm_medium=central_kitchen&utm_campaign=central_kitchen_demo&utm_content=systems_catalog",
    primary_action: "pilot",
    contact_category: "experience_cta",
    contact_label: "experience_solution_view",
    updated_at: "2026-07-13"
  },
  {
    id: "diagnostic_workbench",
    slug: "diagnostic-workbench",
    title: "企業問題診斷與決策交付工作台",
    short_title: "診斷工作台",
    subtitle: "把雜亂經營痛點收成可審閱、可重複驗證的決策交付工作流",
    status: "Design-partner Pilot",
    maturity: "Pilot Ready",
    access_type: "Controlled Sandbox",
    featured: true,
    featured_order: 2,
    category: ["決策交付", "知識治理"],
    industries: ["製造業", "供應鏈", "跨產業"],
    page_variant: "consulting-delivery",
    showcase_type: "report-workflow",
    demo_duration: "30–45 分鐘",
    highlights: [
      "從雜亂經營痛點到結構化診斷章節與決策矩陣",
      "知識匹配保留統計與可解釋理由，顧問負責判斷",
      "正式報告、評估與知識回寫形成完整交付閉環"
    ],
    sections: ["workflow", "report-preview", "knowledge-loop", "boundaries", "pilot-cta"],
    compliance_note: "示範與 Pilot 使用匿名或受控案件資料；公開網站不展示真實客戶內容。",
    cta_text: "查看診斷工作台",
    cta_href: "./diagnostic-workbench/index.html",
    catalog_cta_href: "../diagnostic-workbench/index.html",
    pilot_program_text: "預約 30–45 分鐘 Demo",
    pilot_program_href: "./contact.html?request_type=diagnostic_demo&utm_source=site&utm_medium=workbench&utm_campaign=diagnostic_demo&utm_content=flagship",
    catalog_pilot_program_href: "../contact.html?request_type=diagnostic_demo&utm_source=site&utm_medium=workbench&utm_campaign=diagnostic_demo&utm_content=systems_catalog",
    primary_action: "detail",
    contact_category: "experience_cta",
    contact_label: "experience_solution_view",
    updated_at: "2026-07-13"
  },
  {
    id: "phoenix_auditable_ai_workflow",
    slug: "phoenix-auditable-ai-workflow",
    title: "Phoenix 可稽核 AI 工作流",
    short_title: "開源工作流",
    subtitle: "把政策防護、引用證據、人工覆核與稽核事件組成可檢驗的企業 AI 參考架構",
    status: "Open Source v0.1.0",
    maturity: "Open Source Reference",
    access_type: "Public GitHub / Local Reference",
    featured: true,
    featured_order: 3,
    category: ["AI 治理", "開源參考架構"],
    industries: ["資訊與稽核", "企業治理", "跨產業"],
    page_variant: "governance-reference",
    showcase_type: "open-source-showcase",
    demo_duration: "60–90 秒",
    highlights: [
      "Input 與 Output Policy 規則核對",
      "政策衝突攔截與 Human-in-the-loop 人工覆核",
      "Markdown 引用驗證與可查詢的 SQLite 稽核事件"
    ],
    sections: ["portfolio-chain", "workflow", "evidence", "service-boundary", "audience", "limitations", "pilot-cta"],
    compliance_note: "本機 Mock-first 參考架構；使用合成資料，非生產環境認證，稽核事件不具密碼學不可竄改保證。",
    cta_text: "查看開源系統展示",
    cta_href: "./experience/phoenix-auditable-ai-workflow/index.html",
    catalog_cta_href: "./phoenix-auditable-ai-workflow/index.html",
    pilot_program_text: "預約 AI 治理與導入診斷",
    pilot_program_href: "./contact.html?request_type=auditable_ai_demo&utm_source=site&utm_medium=open_source_showcase&utm_campaign=phoenix_auditable_ai_flow&utm_content=homepage_card",
    catalog_pilot_program_href: "../contact.html?request_type=auditable_ai_demo&utm_source=site&utm_medium=open_source_showcase&utm_campaign=phoenix_auditable_ai_flow&utm_content=systems_catalog",
    primary_action: "pilot",
    contact_category: "experience_cta",
    contact_label: "experience_solution_view",
    updated_at: "2026-07-13"
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = window.EXPERIENCE_SOLUTIONS;
}
