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
      "結構化動作卡依規則自決，或送總部審核例外",
      "核准後產出對客文案與 ERP／POS 沙盒預覽"
    ],
    sections: ["event-flow", "dual-workbench", "tier-ladder", "boundaries", "pilot-cta"],
    compliance_note: "Sandbox Demo；對客通知與 ERP／POS payload 僅為模擬預覽，不寫入正式系統。",
    cta_text: "查看營運防護台",
    cta_href: "./experience/central-kitchen-ai-agent/index.html",
    catalog_cta_href: "./central-kitchen-ai-agent/index.html",
    pilot_program_text: "預約 15 分鐘 Demo",
    pilot_program_href: "https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform?utm_source=site&utm_medium=flagship&utm_campaign=central_kitchen_demo",
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
      "從問題定義到決策矩陣，完整流程留在系統內",
      "AI 加速章節草稿，最終策略判斷由顧問負責",
      "定稿洞見回寫知識模式，讓後續診斷更快對準"
    ],
    sections: ["workflow", "report-preview", "knowledge-loop", "boundaries", "pilot-cta"],
    compliance_note: "示範與 Pilot 使用匿名或受控案件資料；公開網站不展示真實客戶內容。",
    cta_text: "查看診斷工作台",
    cta_href: "./diagnostic-workbench/index.html",
    catalog_cta_href: "../diagnostic-workbench/index.html",
    pilot_program_text: "預約 30–45 分鐘 Demo",
    pilot_program_href: "./contact.html?utm_source=site&utm_medium=flagship&utm_campaign=diagnostic_workbench",
    catalog_pilot_program_href: "../contact.html?utm_source=site&utm_medium=systems_catalog&utm_campaign=diagnostic_workbench",
    contact_category: "experience_cta",
    contact_label: "experience_solution_view",
    updated_at: "2026-07-13"
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = window.EXPERIENCE_SOLUTIONS;
}
