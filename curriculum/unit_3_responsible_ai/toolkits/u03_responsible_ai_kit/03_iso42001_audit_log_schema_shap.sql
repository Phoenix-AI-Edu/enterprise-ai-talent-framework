-- 鳳凰 AI 企業級日誌庫與 SHAP 可解釋性歸因表 DDL
-- 對位 ISO/IEC 42001:2023 控制項 A.9 (AI 系統紀錄與審計)

-- 1. 建立合規審計日誌主表
CREATE TABLE IF NOT EXISTS ai_compliance_audit_log (
    log_id VARCHAR(64) PRIMARY KEY,                   -- 唯一日誌追溯 ID
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- 系統時間截記
    model_name VARCHAR(64) NOT NULL,                  -- 使用的大模型版本 (e.g., Llama-3-70b-instruct)
    use_case VARCHAR(64) NOT NULL,                    -- 應用場景 (e.g., 'AML_Anomaly_Detection', 'Credit_Scoring')
    user_id VARCHAR(64) NOT NULL,                     -- 操作員工編號
    transaction_id VARCHAR(64) NOT NULL,              -- 關聯之交易/客戶紀錄 ID
    prediction_result VARCHAR(32) NOT NULL,           -- AI 判定結果 (e.g., 'High_Risk', 'Low_Risk')
    
    -- 模型信心度指標
    precision_score DOUBLE PRECISION,
    recall_score DOUBLE PRECISION,
    
    -- SHAP (SHapley Additive exPlanations) 可解釋性歸因數據
    shap_base_value DOUBLE PRECISION NOT NULL,        -- SHAP 基準值 (Base Expected Value)
    shap_val_ip_hop DOUBLE PRECISION,                 -- 特徵 1: 跨國 IP 跳變貢獻度
    shap_val_large_integer DOUBLE PRECISION,          -- 特徵 2: 深夜大額整數偏好貢獻度
    shap_val_kyc_deviation DOUBLE PRECISION,          -- 特徵 3: 偏離歷史 KYC 屬性貢獻度
    shap_val_velocity DOUBLE PRECISION,               -- 特徵 4: 資金快進快出速度貢獻度
    
    -- 人機協作 (HITL) 覆核機制
    audit_status VARCHAR(16) DEFAULT 'PENDING',       -- 審核狀態: 'PENDING', 'APPROVED', 'REJECTED'
    reviewer_signature VARCHAR(64)                    -- 合格專員之數位簽章 (如: 分析師憑證號)
);

-- 2. 建立索引以加速後續金管會或內部合規抽查檢索
CREATE INDEX idx_audit_timestamp ON ai_compliance_audit_log(timestamp);
CREATE INDEX idx_audit_use_case ON ai_compliance_audit_log(use_case);
CREATE INDEX idx_audit_status ON ai_compliance_audit_log(audit_status);

-- 3. 測試用 INSERT 範本 (模擬一筆 AI 防制洗錢 AML 判定紀錄)
INSERT INTO ai_compliance_audit_log (
    log_id, 
    model_name, 
    use_case, 
    user_id, 
    transaction_id, 
    prediction_result, 
    shap_base_value, 
    shap_val_ip_hop, 
    shap_val_large_integer, 
    shap_val_kyc_deviation, 
    shap_val_velocity, 
    audit_status, 
    reviewer_signature
) VALUES (
    'AUD-20260618-10048A', 
    'Llama-Guard-3-8B-AML', 
    'AML_Anomaly_Detection', 
    'EMP-8832', 
    'TXN-99823481', 
    'High_Risk', 
    0.15,               -- 模型預設基礎風險機率 15%
    0.45,               -- IP 短時間跨國跳變使風險 +45% (最大特徵)
    0.20,               -- 深夜大額轉帳特徵使風險 +20%
    0.10,               -- 偏離 KYC 屬性使風險 +10%
    0.05,               -- 資金快進快出使風險 +5%
    'APPROVED', 
    'COMPLIANCE_OFFICER_CHOU'
);

-- 4. 稽核查詢範例：調出所有未經人工覆核 (PENDING) 且被 AI 判定為高風險的交易
-- SELECT * FROM ai_compliance_audit_log WHERE prediction_result = 'High_Risk' AND audit_status = 'PENDING';
