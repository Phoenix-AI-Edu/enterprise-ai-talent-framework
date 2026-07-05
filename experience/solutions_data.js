/* experience/solutions_data.js
 * 專屬資料模型，所有內容已去識別化，不含真實客戶、品牌名或系統名稱。
 * Analytics 事件命名對齊 ANALYTICS_EVENT_INVENTORY.md：experience_* family
 */

window.EXPERIENCE_SOLUTIONS = [
  {
    id: "central_kitchen_ai_agent",
    slug: "central-kitchen-ai-agent",
    title: "中央廚房 AI 營運助理",
    subtitle: "餐飲連鎖與零售通路統一營運指揮中心",
    status: "Interactive Demo / Pilot Ready",
    gated_demo: true,
    industries: ["餐飲連鎖", "中央廚房", "零售連鎖"],
    maturity: "Pilot Ready",
    compliance_note: "所有展示場景均為去識別化模擬，不涉及任何真實品牌或ERP/POS系統。",

    cta_text: "預覽互動 Demo",
    cta_href: "#experience/central-kitchen-ai-agent",
    pilot_program_text: "申請參與 Pilot 計畫",
    pilot_program_href: "https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform",

    overview: [
      "總部與門市之間的營運指令傳遞，通常耗時且容易失真。本方案以統一語言層與任務拆解引擎，把每日進貨、備料、出勤與異常通報串聯為自動化工作流。",
      "訪客可進入互動式 Demo，體驗 LINE 門市通報、總部戰情室 KPI 監控、高風險意圖阻斷，以及沙盒 ERP/POS Payload Preview 的對話流程。"
    ],

    highlights: [
      "總部多門市指標集中監控：營收、耗損、溫層異常、結帳高峰與異動告警",
      "門市端 LINE 自然語言提報：免下載 APP，文字/語音直通總部與自動化工單",
      "高風險意圖阻斷：系統先行偵測，再以 Human-in-the-loop 確認高資安任務",
      "RBAC 角色控管：總經理、區域主管、門市店長、品保各有存取邊界",
      "沙盒 ERP/POS Payload Preview：在無真實系統連線前提早驗證接規格"
    ],

    roi_statement: "預期協助企業壓縮營運指令錯誤率、縮短跨層通報時程，並降低紙本與口頭通報造成的人為疏漏。",

    contact_category: "experience_cta",
    contact_label: "solution_view",
    form_intent: "high",
    source_section: "solution_detail",

    consent_text: "點擊提交表單即表示您已詳閱並同意<a href='./privacy.html'>《個人資料保護與隱私權政策告知書》</a>"
  }
];

if (typeof module !== "undefined" && module.exports) {
  module.exports = window.EXPERIENCE_SOLUTIONS;
}
