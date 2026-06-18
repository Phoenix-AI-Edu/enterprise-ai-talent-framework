#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
鳳凰 AI - 企業級地端雙向去識別化與還原管道 
(Reversible De-identification DLP Pipeline)
對位 ISO/IEC 42001 條款 A.7 (資料生命週期) 與 A.9 (系統記錄)

功能：
1. 在資料離開本地企業內網前，自動將台灣身分證、信用卡、手機號碼等精準個資進行 Regex 遮蔽。
2. 利用地端輕量級 NLP (spaCy NER) 識別並遮蔽人名 (PERSON) 與地址 (GPE/LOC)。
3. 將敏感詞彙替換為安全 Token (如 [REDACTED_PERSON_NAME_0])，並將對照表存於本地記憶體/DB。
4. 接收雲端大模型回覆後，利用本地 Token Vault 進行雙向還原，呈現明文給員工。
"""

import re
import spacy
from typing import Dict

class LocalDLPPipeline:
    def __init__(self, spacy_model: str = "zh_core_web_sm"):
        # 1. 初始化繁中 NER 語言模型大腦
        try:
            self.nlp = spacy.load(spacy_model)
            print(f"[DLP Pipeline] 成功載入地端 NER 模型: {spacy_model}")
        except IOError:
            self.nlp = None
            print(f"[DLP Pipeline] 警告: 未能載入地端 NER 模型 ({spacy_model})，請先執行 python -m spacy download {spacy_model}")
            
        # 2. 定義精準的正則表達式規則庫 (台灣專屬特有 PII 格式)
        self.regex_rules = {
            "TAIWAN_ID": re.compile(r'[A-Z][1-2]\d{8}'), # 台灣身分證字號
            "CREDIT_CARD": re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'), # 16位信用卡號
            "BANK_ACCOUNT": re.compile(r'\b\d{3}[- ]?\d{3}[- ]?\d{6,8}\b'), # 銀行帳戶代號
            "MOBILE_PHONE": re.compile(r'\b09\d{2}[- ]?\d{3}[- ]?\d{3}\b'), # 手機號碼
            "EMAIL": re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b') # 電子郵件
        }
        
        # 3. 實體對照表 (Token Vault)：儲存於本地 DMZ 內，嚴禁向外網暴露
        self.token_vault: Dict[str, str] = {}
        
    def _get_synthetic_token(self, original_text: str, category: str) -> str:
        """生成唯一的虛擬替代標籤，若已遮蔽過則沿用相同的 token"""
        for tok, orig in self.token_vault.items():
            if orig == original_text:
                return tok
                
        # 依類別計算當前序號
        index = len([k for k in self.token_vault.keys() if category in k])
        synthetic_token = f"[{category}_TKN_{index}]"
        self.token_vault[synthetic_token] = original_text
        return synthetic_token
        
    def de_identify(self, text: str) -> str:
        """
        【去識別化 (Anonymization)】
        將輸入的原始文本遮蔽為虛擬 Token，並寫入地端 Token Vault。
        """
        if not text:
            return ""
            
        redacted = text
        
        # 第一步：正則表達式掃描 (精準匹配)
        for category, pattern in self.regex_rules.items():
            matches = list(pattern.finditer(redacted))
            # 必須「反向替換」，防止字串長度改變導致偏移錯誤
            for m in sorted(matches, key=lambda x: x.start(), reverse=True):
                original_val = m.group(0)
                synthetic_token = self._get_synthetic_token(original_val, category)
                redacted = redacted[:m.start()] + synthetic_token + redacted[m.end():]
                
        # 第二步：Spacy NER (語境實體識別)
        if self.nlp:
            doc = self.nlp(redacted)
            # 反向替換
            for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
                if ent.label_ == "PERSON":
                    synthetic_token = self._get_synthetic_token(ent.text, "PERSON")
                    redacted = redacted[:ent.start_char] + synthetic_token + redacted[ent.end_char:]
                elif ent.label_ in ["GPE", "LOC"]:
                    synthetic_token = self._get_synthetic_token(ent.text, "ADDRESS")
                    redacted = redacted[:ent.start_char] + synthetic_token + redacted[ent.end_char:]
                    
        return redacted
        
    def re_identify(self, anonymized_text: str) -> str:
        """
        【重識別/還原 (De-anonymization)】
        將大模型輸出的含 Token 文本，在地端還原為真實個資。
        """
        if not anonymized_text:
            return ""
            
        restored = anonymized_text
        # 按 token 長度反向排序，避免長度短的 token (如 _1) 提早被部分替換
        sorted_tokens = sorted(self.token_vault.keys(), key=len, reverse=True)
        for token in sorted_tokens:
            restored = restored.replace(token, self.token_vault[token])
        return restored
        
    def clear_vault(self):
        """定期物理清理 Token Vault，符合合規銷毀規範"""
        self.token_vault.clear()

if __name__ == "__main__":
    # 初始化
    dlp = LocalDLPPipeline()
    
    # 模擬員工提問
    raw_input = "請協助查詢客戶陳建宇 (身分證 A123456789，電話 0912-345-678) 住在台北市大安區信義路，其綁定卡號 4311-9527-1234-5678 的最新回饋點數。"
    
    print("\n========== 🔒 地端去識別化流程 (送出前) ==========")
    print(f"【原始明文】: {raw_input}")
    
    safe_prompt = dlp.de_identify(raw_input)
    print(f"【安全遮罩】: {safe_prompt}")
    
    print("\n【Token Vault 本地保險箱狀態】:")
    for token, orig in dlp.token_vault.items():
        print(f"  {token} ➔ {orig}")
        
    # 模擬雲端大模型收到安全遮罩後的回答
    print("\n========== ☁️ 雲端大模型處理 ==========")
    llm_completion = "針對客戶 [PERSON_TKN_0] (身分證 [TAIWAN_ID_TKN_0]) 之申請，我們已核對其居住地 [ADDRESS_TKN_0]。系統顯示綁定卡片 [CREDIT_CARD_TKN_0] 的最新回饋點數為 1,250 點，請撥打 [MOBILE_PHONE_TKN_0] 通知客戶。"
    print(f"【大模型原始輸出】: {llm_completion}")
    
    # 在地端解密還原
    print("\n========== 🔓 安全地端重識別還原 (接收後) ==========")
    restored_output = dlp.re_identify(llm_completion)
    print(f"【員工終端機顯示】: {restored_output}")
