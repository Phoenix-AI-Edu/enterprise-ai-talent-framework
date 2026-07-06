# 鳳凰 AI 中央廚房行銷：UTM 結構規範 v0.2.0

> 定義第一波對外文宣的追蹤參數，確保分群歸因。

---

## URL 顯示格式

```
<BASE_URL>?utm_source=<channel>&utm_medium=<medium>&utm_campaign=<campaign>
```

## Base Rules

- BASE_URL 統一為：
  `https://phoenix-ai-edu.github.io/enterprise-ai-talent-framework/experience/central-kitchen-ai-agent/`
- 不得直接導 Google Form，Landing page 內才含二層 Form CTA。
- 第一波 campaign 固定為 `v020_central_kitchen_ai`。
- private/form 導向不附加 UTM。
- email 正文使用短連結並保留 UTM。

---

## Source/Medium/Campaign Matrix

| 渠道 | utm_source | utm_medium | utm_campaign | 說明 |
|---|---|---|---|---|
| LinkedIn 貼文 | linkedin | social | v020_central_kitchen_ai | 品牌/個人帳共用參數，內容以文字註記區分 |
| LinkedIn 私訊 | bd_dm | direct | v020_central_kitchen_ai | 可額外 append `&utm_content=dm_v1` |
| Facebook | facebook | social | v020_central_kitchen_ai | 第一波暫不發布 |
| Threads | threads | social | v020_central_kitchen_ai | 第一波暫不發布 |
| One-pager QR | onepager | print | v020_central_kitchen_ai | QR 若印製則 print；web PDF 則 web |
| Email / 信 | email | email | v020_central_kitchen_ai | 視追蹤需求加 `?utm_content=welcome` |
| 官網導覽加碼短連結 | internal | internal | v020_central_kitchen_ai | Gated experience 內 |

---

## Channel Tactic

| 欄位 | LinkedIn 貼文 | BD 私訊 | One-pager | 官網內 |
|---|---|---|---|---|
| Primary CTA | 中央廚房 landing | 中央廚房 landing | 中央廚房 landing | 表單 / 體驗 |
| Secondary CTA | 無 / 留言交流 | 第二段才放表單 | QR / 短連結 | 申請 Demo / 預約諮詢 |
| UTM suffix 需求 | 無 | `&utm_content=dm_v1`（可選） | 無 | 無 |

---

## 建構範例

- LinkedIn：`.../central-kitchen-ai-agent/?utm_source=linkedin&utm_medium=social&utm_campaign=v020_central_kitchen_ai`
- BD 私訊：`.../central-kitchen-ai-agent/?utm_source=bd_dm&utm_medium=direct&utm_campaign=v020_central_kitchen_ai&utm_content=dm_v1`
- Facebook/Threads：同 LinkedIn 但 source 替換為對應字串
- Email：同 LinkedIn 但 medium=email

---

## Analytics Event Names 對應（預留）

- `experience_solution_view`：在 central-kitchen 頁已定義，解除 gated 後生效
- `experience_demo_request_click`：表單 CTA 點擊
- `experience_contact_click`：諮詢 CTA 點擊

> 實際 GA4 report 必須手動建立相對應 events；repo 僅負責 emit。
