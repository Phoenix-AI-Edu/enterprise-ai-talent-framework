/* experience/solutions_data.js
 * 專屬資料模型，所有內容已去識別化，不含真實客戶、品牌名或系統名稱。
 * Analytics 事件命名對齊 ANALYTICS_EVENT_INVENTORY.md：experience_* family
 */

window.EXPERIENCE_SOLUTIONS = [
  {
    id: "central_kitchen_ai_agent",
    slug: "central-kitchen-ai-agent",
    title: "中央廚房營運防護台",
    subtitle: "門市自助查詢、高風險攔截、總部集中審核",
    status: "公開沙盒示範",
    gated_demo: true,
    industries: ["餐飲連鎖", "中央廚房", "零售連鎖"],
    maturity: "Sandbox Demo / Pilot",
    compliance_note: "所有展示場景均為去識別化模擬，不涉及任何真實品牌或ERP/POS系統。",

    cta_text: "看 75 秒流程",
    cta_href: "./central-kitchen-ai-agent/index.html#flow-video",
    pilot_program_text: "申請操作 Demo",
    pilot_program_href: "https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform",

    overview: [
      "這是鳳凰 AI 顧問的可公開旗艦示範案例，用來驗證門市與總部之間的可控營運流程。",
      "公開展示包含查詢、高風險攔截、人工審核與 ERP/POS 沙盒預覽；正式串接屬後續導入專案。"
    ],

    highlights: [
      "門市查詢訂單與庫存，減少電話與群組往返",
      "報廢、取消等高風險操作先攔截並建立審核單",
      "總部核准或拒絕，保留人機協作的決策節點",
      "核准後產生 ERP/POS 沙盒 payload 預覽，不寫入正式系統"
    ],

    roi_statement: "PoC 將以門市查詢改走系統、高風險提報改走審核、總部每週完成至少一筆審核作為驗證標準。",

    contact_category: "experience_cta",
    contact_label: "experience_solution_view",
    form_intent: "high",
    source_section: "solution_detail",

    consent_text: "點擊提交表單即表示您已詳閱並同意<a href='../privacy.html'>《個人資料保護與隱私權政策告知書》</a>"
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = window.EXPERIENCE_SOLUTIONS;
}
