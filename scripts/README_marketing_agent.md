# 鳳凰 AI B2B 行銷自動化 Agent 使用指南 (README_marketing_agent)

本 Agent 專門用於將 B2B 客戶方案建議書或特定技術主題，全自動轉化為 LinkedIn、Facebook、YouTube、X (Twitter) 與 EDM 的專業行銷文案，並在儲存前自動通過本地金融與品牌防線（對齊 `MARKETING_COMPLIANCE_RULES.md`）。

---

## 🚀 快速開始

### 1. 配置 API 金鑰
請確保您的 `OPENAI_API_KEY` 或 `GOOGLE_API_KEY` 已設定。
Agent 會自動在以下路徑尋找並讀取 `.env` 檔案：
1. 當前目錄 `.env`
2. `scripts/.env`
3. 聯動的 microservice 開發目錄 `C:/Users/Ring/Documents/GitHub/twstock/ai_microservice_production/.env` (若存在且有權限)

### 2. 執行指令

#### (A) 針對現有客戶建议書生成全渠道行銷內容
```bash
# 生成 henda (恆達精密) 的所有渠道文案
python scripts/marketing_agent.py --client henda --platforms all
```

#### (B) 針對特定行銷主題進行生成
```bash
# 生成特定主題的 LinkedIn 與 X 推文
python scripts/marketing_agent.py --topic "ISO 42001 企業稽核避坑指引" --platforms linkedin,twitter
```

### 3. 主要參數說明

| 參數 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `--client` | `None` | 客戶方案名稱，如 `henda`, `securities` (自動讀取對應的 `proposal_[client].md` 作為背景) |
| `--topic` | `None` | 自訂行銷主題 (與 `--client` 二選一) |
| `--platforms` | `all` | 要產出的平台，多個平台用逗號分隔，可選: `linkedin`, `facebook`, `youtube`, `twitter`, `edm` |
| `--output_dir` | `marketing_drafts` | 生成文案的草稿目錄 |
| `--model` | `None` | 指定模型名稱 (如 `gemini-2.0-flash` 或 `gpt-4o-mini`) |

---

## 🛡️ 合規守門員 (Compliance Guardian)

本 Agent 內建雙重合規檢測：
1. **金融紅線阻斷 (Hard Block)**：偵測到如「保證獲利」、「穩賺不賠」、「買進/賣出」等投資推介敏感詞時，會在主報告中發出顯著警告，提醒行銷專員手動移除。
2. **內部代號隔離 (Auto-Replace)**：自動將非公開的內部系統代號進行商業化正名替換：
   - `OpenClaw` ➔ **企業 AI 微服務架構**
   - `HITL` ➔ **有人在環 (Human-In-The-Loop) 協作流程**
   - `Compliance Pipeline` ➔ **自動化合規審查防線**
   - `Virtual Compliance Guardian` ➔ **虛擬合規官**
