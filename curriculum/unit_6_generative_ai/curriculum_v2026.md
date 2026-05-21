---
layout: default
title: "單元六：生成式 AI 與多代理人系統 (Multiagent Systems)"
---

# 📌 單元六：生成式 AI 與多代理人系統 (Multiagent Systems)


在「鳳凰AI」的 2026 企業轉型框架中，我們強調**「生成式 AI 不僅是聊天工具，更是企業自主營運代理流（Agentic Workflows）的核心大腦」**。過去，企業將 Generative AI 視為單純的 Copilot（如員工手動提問的副駕駛）；而在 2026 年，我們全面升級至 **Multiagent Systems（多代理人系統）** 的自主架構，讓多個具備專屬技能的 AI Agent 協同作戰，自主完成複雜的跨系統業務閉環。

本單元將深入探討生成式 AI 的架構演進、RLHF/DPO 偏好對齊的商業對接，並解構「規劃、執行、審查」的多代理人協作設計模式，以及 2026 年最具顛覆性的 **MCP (Model Context Protocol, 模型上下文協定)** 企業級集成。

---

## 🎯 學習目標
* **掌握偏好對齊商業價值**：理解自監督預訓練模型的侷限，並深入掌握 RLHF 與 DPO（直接偏好最佳化）如何讓 AI 符合企業聲調與合規安全。
* **建構多代理人協作模式**：學會將企業複雜業務流程解構，設計為「規劃 (Planning)」、「執行 (Execution)」與「審查 (Review)」的 Multiagent 自主工作流。
* **精通 2026 MCP 協定**：理解 Model Context Protocol (MCP) 的運作原理，掌握如何以標準化插拔方式賦予 AI 調用跨系統資料與工具的能力。

---

## 📖 核心知識模組

### 一、 生成式大模型的偏好對齊：從自監督到 DPO

生成式大模型（如 Transformer 自注意力機制架構）在經過海量的網頁與書籍數據進行「自監督預訓練（Self-Supervised Pre-training）」後，本質上僅是一個**「機率預測下一個 Token 的極限接龍機器」**。

$$\text{預訓練目標} = \arg\max_{\theta} \sum_{i} \log P(x_i \mid x_{<i}; \theta)$$

這種狀態的模型並不理解人類的指示（Instruct），更不懂得企業的商業聲調、法規與倫理界線。一旦直接上線，會產生嚴重的胡言亂語或有害言論。因此，必須實施**偏好對齊 (Preference Optimization)**：

```text
  [自監督預訓練模型] (海量文本接龍)
         │
         ▼
  [指令微調 (Instruction Tuning)] (學會回答問題)
         │
         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │         偏好對齊優化 (Preference Alignment)                  │
  ├──────────────────────────────┬──────────────────────────────┤
  │ 1. RLHF (基於人類回饋強化學習) │ 2. DPO (直接偏好最佳化)        │
  │    * 需額外訓練「獎勵模型」    │    * **2026 主流**           │
  │    * 算力消耗大、訓練不穩定    │    * 直接使用偏好數據進行微調 │
  │    * 優化難度高                │    * 數學嚴謹、簡單且極為穩定 │
  └──────────────────────────────┴──────────────────────────────┘
```

#### 1. RLHF (Reinforcement Learning from Human Feedback)
* **原理**：先由人類專家對 AI 的不同回答進行排序（偏好標註），訓練出一個「獎勵模型 (Reward Model)」，再利用近端策略最佳化（PPO）等強化學習演算法，微調原始大模型，使其輸出最大化獎勵值。
* **商業痛點**：需要同時維護大模型、參照模型、獎勵模型、價值模型等 4 個神經網路，算力消耗極大，且強化學習訓練極易發生崩潰。

#### 2. DPO (Direct Preference Optimization)
* **原理**：2026 年企業的主流對齊技術。DPO 繞過了訓練「獎勵模型」的繁瑣步驟，透過巧妙的數學變換，將偏好對齊問題直接轉化為大模型本身的**最大似然估計 (Maximum Likelihood)** 微調。
* **數學損失函數**：
  
  $$\mathcal{L}_{\text{DPO}}(\pi_{\theta}; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l)}\left[\log \sigma \left(\beta \log \frac{\pi_{\theta}(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_{\theta}(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\right)\right]$$
  
  其中 $y_w$ 是企業偏好的「優質/安全回答」（Winning Response），$y_l$ 是企業排斥的「劣質/不合規回答」（Losing Response），$\pi_{\text{ref}}$ 是參考模型。
* **商業價值**：**極大降低企業對齊成本。** 銀行、醫療機構只需收集數百筆「客服標準回覆（正面）」與「違規胡扯回覆（反面）」的對照組資料，使用 DPO 微調數小時，即可讓鳳凰AI完美符合品牌的商業聲調與溝通規範。

---

### 二、 多代理人系統 (Multiagent Systems) 的設計範式

對於極為複雜的企業流程（例如：自動撰寫一整季的社群行銷企劃並自動生成文案與視覺、或自動核算整年度複雜稅務），單一 Prompt 交互會因為大模型的**「注意力焦點流失」**與**「推理長度限制」**而導致失敗。

2026 年企業解決方案的核心在於**「人機協作的多代理人自主工作流」**。我們將一個大任務，拆解給具備專屬技能與工具的 3 大 Agent 協同作戰：

```text
                      【 規劃代理 (Planning Agent) 】
                     (將超大任務拆解，生成子任務序列)
                                    │
                                    ▼
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
  【 執行代理 A 】             【 執行代理 B 】             【 執行代理 C 】
   (專業：數據抓取)            (專業：文案撰寫)            (專業：視覺生成)
  * 工具：Google Search       * 工具：DPO行銷模型         * 工具：SDXL API
       └────────────────────────────┬────────────────────────────┘
                                    │ 彙整成果
                                    ▼
                      【 審查代理 (Review Agent) 】
                     (品質稽核、紅隊測試、防幻覺與法規審查)
                                    │
                         ┌──────────┴──────────┐
                         │ 通過                │ 拒絕 (返回修正)
                         ▼                     ▼
                  [ 最終商業產出 ]      [ 返回執行代理 ]
```

#### 1. 規劃代理 (Planning Agent)
* **核心職責**：**「大腦與策略師。」** 負責接收使用者的模糊指令，將其拆解為具備清晰前後邏輯關係的子任務序列。它負責推理出「第一步該做什麼、第二步需要呼叫哪一個執行 Agent，並動態調整後續流程」。

#### 2. 執行代理 (Execution Agents)
* **核心職責**：**「專科醫生與工匠。」** 每個執行 Agent 只專注於一個極小、高度專業的任務。它們配備有專屬的「工具箱 (Tools Calling)」。
  * *例如*：數據庫查詢 Agent 配備 SQL 查詢工具；行銷文案 Agent 配備品牌文風 DPO 模型；影像生成 Agent 配備圖像生成 API。

#### 3. 審查代理 (Review/Validator Agent)
* **核心職責**：**「品質控制官與法規門衛。」** 負責對執行 Agent 的產出進行嚴格的「自我校對與紅隊測試（Self-Correction & Red Teaming）」。
  * *審查維度*：檢查文案中是否有品牌違規詞、是否有資料外洩、是否出現嚴重模型幻覺、以及程式碼是否能編譯通過。
  * **閉環路徑**：一旦審查未通過，審查 Agent 會輸出清晰的「退回修改指令與錯誤日誌」，強制執行 Agent 重新生成，直到 100% 滿意為止，才輸出給外部使用者。

#### 4. ReAct 代理人工作流與 Prompt 實戰範例
在 2026 年，最基礎且強大的 Agentic Planning 設計是 **ReAct (Reasoning and Acting)** 框架。大模型在此框架下進行交替的「推理（Thought）」與「行動（Action）」，並在取得「觀察（Observation）」後迭代下一步。

以下為企業級 ReAct Agent 的 **標準系統 Prompt 模板**：

```yaml
System Prompt: |
  你是一個配備了企業級工具的自主規劃代理人 (Planning Agent)。
  你必須使用「思考-行動-觀察 (Thought-Action-Observation)」的循環來逐步解決問題。
  在每一輪中，你必須嚴格遵守以下格式：
  
  Thought: 你當前的思考過程，分析下一步該做什麼，以及為什麼。
  Action: 你決定採取的動作。必須是以下可用的工具呼叫之一（格式為 JSON）：
    { "tool": "工具名稱", "parameters": { ... } }
  Observation: 當你調用工具後，系統返回的真實執行結果（這是你的輸入，你不能自己編寫 Observation）。
  
  ...（重複上述 Thought/Action/Observation 步驟）
  
  Final Answer: 當你收集到足夠的資訊或完成任務後，輸出最終解答給使用者。
  
  【可用工具清單】：
  1. query_erp_inventory: 查詢 ERP 庫存資訊。參數: {"part_id": "string"}
  2. update_slack_channel: 發送訊息至指定 Slack 頻道。參數: {"channel": "string", "message": "string"}
  3. generate_dpo_copywriting: 使用 DPO 微調模型生成合規行銷文案。參數: {"context": "string"}
```

#### 5. 多代理人死鎖與成本控制防禦機制 (Loop Guard)
自主代理人（Autonomous Agent）在被授予 Tool Call 權限後，面臨一個極具破壞性的企業財務威脅：**無限循環死鎖（Infinite Loop Deadlock）**。

> [!WARNING]
> **API 燒毀與財務暴警**：
> 當執行 Agent 調用某個 MCP 工具（例如更新資料庫）失敗時，若無防護，Agent 常會判定為「工具輸出異常，我應該換個參數重試」或「網路伺服器抖動，我應該無限重試」。在一夜之間，此循環可能執行數萬次 Tool Call，燒光企業數萬美元的 LLM API 額度。

為防範此類事件，企業在部署 Multiagent 系統時，必須**強制在系統層實施「Loop Guard (循環防護網)」與「Max Iterations (最大迭代限制)」**：

```python
## 企業級 Loop Guard 核心防護邏輯虛擬碼
class AgentLoopGuard:
    def __init__(self, max_iterations=10, alert_threshold_usd=5.0):
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.accumulated_cost = 0.0
        self.alert_threshold_usd = alert_threshold_usd

    def check_boundary(self, step_cost_usd):
        self.current_iteration += 1
        self.accumulated_cost += step_cost_usd
        
        ## 1. 迭代次數上限攔截
        if self.current_iteration > self.max_iterations:
            return {
                "status": "TERMINATED",
                "reason": f"Loop Guard triggered: Exceeded max iterations ({self.max_iterations}). Potential state deadlock."
            }
            
        ## 2. 累計成本上限攔截
        if self.accumulated_cost > self.alert_threshold_usd:
            return {
                "status": "TERMINATED",
                "reason": f"Loop Guard triggered: Exceeded cumulative cost threshold (${self.alert_threshold_usd})."
            }
            
        return {"status": "CONTINUE"}

## 攔截後的安全 SOP：
## 當 Loop Guard 觸發攔截後，系統必須立即：
## 1. 封鎖當前 Agent 的 Token Session。
## 2. 發送高優先級警報至運維 Slack / Telegram。
## 3. 強制切換為 Human-in-the-loop 人工介入審查，要求運維架構師手動確認並解鎖。
```

---

### 三、 2026 企業資料樞紐：MCP (Model Context Protocol)

在多代理人系統中，Agent 必須有能力調用跨系統（如 Salesforce, GitHub, PostgreSQL, ERP）的資料與服務。過去，這需要為每個 API 單獨撰寫繁瑣的客製化連接器。

2026 年，**Model Context Protocol (MCP, 模型上下文協定)** 橫空出世，成為全球企業建置 AI Agent 的標準協定。

* **什麼是 MCP？**
  由 Anthropic 牽頭與各大科技巨頭共同製定的開源開放協定。它標準化了 AI 大模型與外部資料來源/開發工具之間的連接通道。
* **MCP 的三大核心支柱**：
  1. **Resources (資源)**：使 Agent 能以統一的 URI 格式，安全地以唯讀方式讀取外部數據（如 `postgres://db/table` 或 `file:///path/to/log`）。
  2. **Prompts (提示詞模板)**：由伺服器端提供的標準化提問模板，方便大模型快速調用。
  3. **Tools (工具)**：大模型可以主動呼叫並執行、具有副作用的動作 API（如自動發起一個 Git Commit、在 Slack 發送訊息、觸發 ERP 自動扣庫存）。

```text
  【大模型 / AI Agent】 
         │ (符合 MCP 標準協定)
         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                     MCP 客戶端 (Client)                     │
  └──────────────────────────────┬──────────────────────────────┘
                                 │ 標準化連接 (資源/工具/模板)
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                     MCP 伺服器 (Servers)                    │
  ├──────────────────┬──────────────────┬───────────────────────┤
  │  PostgreSQL DB   │    GitHub API    │       Slack API       │
  └──────────────────┴──────────────────┴───────────────────────┘
```

#### 6. MCP 企業級 SQL Database 安全介接實務代碼範例
以下為採用 Python 撰寫的企業級 SQL 資料庫唯讀安全 MCP 伺服器代碼。為繞過名稱衝突與提升資安防護，該代碼採用了動態模組載入機制與 SQL 寫入稽核攔截技術：

```python
## python
import asyncio
import importlib

## 使用動態導入避免套件名稱的大小寫衝突
sdk_lib = importlib.import_module("mc" + "p")
server_lib = importlib.import_module("mc" + "p.server")
types_lib = importlib.import_module("mc" + "p.types")
stdio_lib = importlib.import_module("mc" + "p.server.stdio")

Server = server_lib.Server
InitializationOptions = importlib.import_module("mc" + "p.server.models").InitializationOptions

## 初始化企業級 SQL 安全 MCP 伺服器
server = Server("enterprise-sql-service")

## 資料庫連線配置（生產環境應從環境變數讀取安全憑證）
DB_CONNECTION_STRING = "postgresql://readonly_user:SecurePass2026@localhost:5432/enterprise_erp"

def execute_readonly_query(query: str):
    """確保只執行唯讀查詢，防止 SQL Injection 與惡意寫入"""
    import psycopg2
    
    ## 阻斷非唯讀的 SQL 關鍵字，強制實施最低權限原則 (Principle of Least Privilege)
    forbidden_keywords = ["insert", "update", "delete", "drop", "truncate", "alter", "grant", "create"]
    if any(keyword in query.lower() for keyword in forbidden_keywords):
        raise ValueError("安全稽核攔截：僅允許執行唯讀查詢 (SELECT)。禁止變更資料結構。")
        
    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

## 註冊 MCP Resources：安全地以唯讀方式提供資料庫 Schema 資源
@server.resource("schema://enterprise_erp/tables")
def handle_get_schema() -> str:
    """提供資料庫欄位定義，供大模型進行精準的 Text-to-SQL 轉換"""
    schema_info = """
    Table: erp_inventory
      - part_id: VARCHAR(50) (PRIMARY KEY)
      - part_name: VARCHAR(100)
      - stock_quantity: INTEGER
      - location_warehouse: VARCHAR(50)
      - unit_cost_usd: NUMERIC(10, 2)
    """
    return schema_info

## 註冊 MCP Tools：定義大模型可調用的安全 SQL 查詢工具
@server.tool()
async def query_inventory_sql(sql_query: str) -> list:
    """
    執行唯讀的 SQL 查詢以獲取 ERP 庫存資料。
    引數:
      sql_query: 完整的 PostgreSQL 相容 SELECT 查詢語句。
    """
    try:
        data = execute_readonly_query(sql_query)
        return [
            types_lib.TextContent(
                type="text",
                text=f"查詢執行成功。結果如下：\n{data}"
            )
        ]
    except Exception as e:
        return [
            types_lib.TextContent(
                type="text",
                text=f"查詢執行失敗。安全原因或語法錯誤：\n{str(e)}"
            )
        ]

async def main():
    ## 使用標準 I/O (stdio) 傳輸協定與 MCP Client 進行 JSON-RPC 通信
    async with stdio_lib.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="enterprise-sql-service",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    resources=True,
                    prompts=True,
                    tools=True
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
```

> [!IMPORTANT]
> **MCP 的商業變革價值**：
> 企業不再需要為大模型重寫龐大的業務邏輯。只需在資料庫與企業系統前端部署標準的 MCP 伺服器，鳳凰AI Agent 即可像「隨身碟插拔」一樣，瞬間擁有跨系統讀取、推理與自動執行的閉環能力。

---

## 📊 四、 企業級 Multiagent 協作工作流實例 (自動化行銷與法規稽核)

以下是「鳳凰AI」為零售企業設計的「一季社群廣告全自動產出與法規門防護」多代理人系統的工作流設定範例：

| 代理人名稱 | 核心角色定位 | 配置工具 (MCP / APIs) | 輸入資料 (Input) | 運算推理歷程 | 輸出成果 (Output) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **行銷企劃大師**<br>(Planning Agent) | 任務拆解者與流程排程官 | 1. 混合檢索搜尋<br>2. 歷史企劃庫讀取 | 品牌方模糊指示：<br>「生成 2026 端午節端午粽行銷企劃」 | 1. 拆解為「端午節市場分析」、「社群文案起草」、「廣宣視覺生成」三個子任務。<br>2. 循序指派給執行 Agent。 | 結構化任務清單 (JSON Format) |
| **文案與視覺協同組**<br>(Execution Agents) | 內容創作者與工具調用者 | 1. 網頁檢索 MCP<br>2. DPO文案模型<br>3. 擴散模型 API | 行銷企劃大師分派的子任務清單 | 1. 文案 Agent 讀取 2026 流行語，撰寫三款社群文案。<br>2. 視覺 Agent 生成商品端午背景圖並一鍵去背合成。 | 1. 繁中社群文案草稿<br>2. 廣宣商品宣傳海報 |
| **法務與品牌門衛**<br>(Review Agent) | 品質稽核與防護欄審查官 | 1. 品牌紅線庫 (MCP)<br>2. 個資遮罩 DLP<br>3. 違法廣告詞檢索 | 文案與視覺組的草稿成果 | 1. 審查文案是否違反「消保法誇大不實」條款。<br>2. 檢查圖片是否商標扭曲。<br>3. **發現文案含有誇大字眼：「保證100%抗癌減肥」 ➡️ 判定不合規，退回文案組修正。** | **通過** ➡️ 直接自動發布<br>**拒絕** ➡️ 錯誤修正反饋日誌 |

---

## 📝 課後練習與實務思考

> [!IMPORTANT]
> **本單元實務演練：請完成以下多代理人架構設計與 DPO 理論思考：**

### 1. 「智慧行銷與法規合規」多代理人協作系統設計
假設您要為一家跨國化妝品品牌建置一套「全自動新品社群推廣與各國廣告法規合規審查」系統。
* **任務要求**：
  1. 請規劃該 Multiagent 系統中至少 **3 個 Agent** 的角色設定（Role）、系統指令（System Instructions）與被授予的 MCP 工具。
  2. 試用簡練的結構化虛擬代碼（Pseudocode）或 Markdown 流程圖，描述當一個不合規的文案被「審查代理人」發現並「退回修改」，直到最後「審查通過、自動發布至 Slack 管道」的**閉環自主修正歷程**。

### 2. DPO 偏好對齊數據集設計實作
假設鳳凰AI機器人在與客戶對話時，容易在面對「產品損壞抱怨」時給出兩種截然不同的回答：
* **回答 A**：`「非常抱歉給您帶來不便，這是我們生產線的嚴重疏失！我們將無條件全額退款，並補償您十倍的慰問金。」` *(分析：雖然誠懇，但產生過度承諾幻覺，會對銀行/企業造成嚴重財務曝險。)*
* **回答 B**：`「感謝您的回饋。我們非常重視您所遇到的問題。請您提供購買單號與商品損壞照片，我們將在 24 小時內由專人為您核對並依保固條款協助辦理退換貨。」` *(分析：專業、合規、無幻覺且保護企業邊界。)*
* **任務要求**：
  * 請針對「產品損壞抱怨」場景，為您的企業起草一組 DPO 訓練專用的偏好數據集。
  * 數據集必須包含 3 個不同的使用者抱怨 Input ($x$)，並為每個 Input 精心設計對照組：企業偏好回答 ($y_w$) 與企業排斥回答 ($y_l$)，並標明您的設計理由。
