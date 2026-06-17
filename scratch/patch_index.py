# -*- coding: utf-8 -*-
import os

def patch_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, "index.html")
    
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found.")
        return
        
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    start_marker = "      <!-- 奢華字卡展區 (Luxury Case Cards Showcase) -->"
    end_marker = "      <!-- 線上修改提示與白皮書 CTA -->"
    
    if start_marker not in html:
        print("Error: start marker not found in index.html")
        return
    if end_marker not in html:
        print("Error: end marker not found in index.html")
        return
        
    parts = html.split(start_marker)
    first_part = parts[0]
    rest = parts[1]
    
    subparts = rest.split(end_marker)
    second_part = subparts[1]
    
    # Define the replacement block
    replacement_block = """<!-- 奢華字卡展區 (Luxury Case Cards Showcase) -->
      <style>
        .cases-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 30px;
          margin-top: 40px;
          margin-bottom: 40px;
        }
        @media (max-width: 1024px) {
          .cases-grid {
            grid-template-columns: repeat(2, 1fr);
          }
        }
        @media (max-width: 768px) {
          .cases-grid {
            grid-template-columns: 1fr;
          }
        }

        .case-card {
          position: relative;
          background: linear-gradient(135deg, rgba(26, 26, 58, 0.45) 0%, rgba(18, 18, 38, 0.75) 100%);
          border: 1px solid var(--glass-border);
          border-radius: 24px;
          padding: 32px;
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
          transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
          display: flex;
          flex-direction: column;
          height: 100%;
        }
        .case-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 4px;
          background: linear-gradient(90deg, var(--phoenix-teal), var(--phoenix-accent));
          opacity: 0;
          transition: opacity 0.3s ease;
          border-radius: 24px 24px 0 0;
        }
        .case-card:hover::before {
          opacity: 1;
        }
        .case-card:hover {
          transform: translateY(-8px);
          border-color: rgba(0, 242, 254, 0.3);
          box-shadow: 0 30px 60px rgba(0, 242, 254, 0.08);
        }

        .case-header {
          display: flex;
          flex-direction: column;
          gap: 12px;
          margin-bottom: 20px;
        }
        .case-id-badges {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }
        .case-id {
          font-family: var(--font-display);
          font-size: 12px;
          font-weight: 700;
          color: var(--phoenix-gold);
          background: rgba(245, 166, 35, 0.08);
          padding: 4px 10px;
          border-radius: 6px;
          border: 1px solid rgba(245, 166, 35, 0.2);
          letter-spacing: 0.5px;
        }
        .case-tag {
          font-size: 11px;
          font-weight: 600;
          color: var(--phoenix-teal);
          background: rgba(0, 242, 254, 0.05);
          padding: 4px 10px;
          border-radius: 30px;
          border: 1px solid rgba(0, 242, 254, 0.15);
        }
        .case-title {
          font-family: var(--font-display);
          font-size: 19px;
          font-weight: 700;
          color: var(--white);
          line-height: 1.4;
          margin-top: 4px;
        }

        .case-divider {
          height: 1px;
          background: rgba(255, 255, 255, 0.05);
          margin-bottom: 20px;
        }

        .case-body {
          display: flex;
          flex-direction: column;
          gap: 18px;
          flex-grow: 1;
        }
        .case-section {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .case-section-title {
          font-size: 12.5px;
          font-weight: 700;
          color: var(--gray-400);
          text-transform: uppercase;
          letter-spacing: 0.8px;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .case-section-content {
          font-size: 13.5px;
          color: var(--gray-300);
          line-height: 1.6;
        }
        .case-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .case-list-item {
          position: relative;
          padding-left: 18px;
          font-size: 13.5px;
          line-height: 1.5;
          color: var(--gray-300);
        }
        .case-list-item::before {
          content: '✦';
          position: absolute;
          left: 0;
          color: var(--phoenix-accent);
          font-size: 12px;
        }
        .case-list-item.solution::before {
          color: var(--phoenix-teal);
        }

        .case-roi-box {
          background: linear-gradient(135deg, rgba(245, 166, 35, 0.08) 0%, rgba(245, 166, 35, 0.02) 100%);
          border: 1px dashed rgba(245, 166, 35, 0.3);
          border-radius: 16px;
          padding: 18px;
          margin-top: 6px;
        }
        .case-roi-title {
          font-size: 13px;
          font-weight: 800;
          color: var(--phoenix-gold);
          margin-bottom: 8px;
          display: flex;
          align-items: center;
          gap: 6px;
          letter-spacing: 0.5px;
        }
        .case-roi-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .case-roi-item {
          position: relative;
          padding-left: 18px;
          font-size: 13px;
          color: var(--white);
          line-height: 1.5;
        }
        .case-roi-item strong {
          color: var(--phoenix-gold);
        }
        .case-roi-item::before {
          content: '🏆';
          position: absolute;
          left: 0;
          font-size: 12px;
        }

        .case-footer {
          margin-top: 24px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .case-target-scheme {
          display: flex;
          align-items: center;
          justify-content: space-between;
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid rgba(255, 255, 255, 0.04);
          padding: 10px 14px;
          border-radius: 12px;
          font-size: 12.5px;
        }
        .scheme-label {
          color: var(--gray-400);
        }
        .scheme-value {
          color: var(--phoenix-gold);
          font-weight: 700;
          font-family: var(--font-display);
        }
        .case-btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          width: 100%;
          padding: 12px 20px;
          border-radius: 12px;
          font-size: 13.5px;
          font-weight: 600;
          transition: all 0.25s ease;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.08);
          color: var(--gray-300);
          text-decoration: none;
        }
        .case-card:hover .case-btn {
          background: linear-gradient(135deg, var(--phoenix-accent) 0%, rgba(233, 69, 96, 0.7) 100%);
          border-color: transparent;
          color: var(--white);
          box-shadow: 0 10px 20px rgba(233, 69, 96, 0.2);
        }
        .case-btn:hover {
          transform: translateY(-2px);
        }
        
        .cases-note-block {
          display: grid;
          grid-template-columns: 2.2fr 1fr;
          gap: 24px;
          margin-top: 32px;
          align-items: center;
          background: rgba(255, 255, 255, 0.01);
          border: 1px solid var(--glass-border);
          padding: 24px;
          border-radius: 16px;
          backdrop-filter: blur(8px);
        }
        @media (max-width: 768px) {
          .cases-note-block {
            grid-template-columns: 1fr;
            text-align: center;
          }
          .cases-note-block div {
            text-align: center;
          }
          .cases-note-block div:last-child {
            text-align: center;
          }
        }

        /* Tabs styling */
        .case-filters {
          display: flex;
          justify-content: center;
          gap: 12px;
          flex-wrap: wrap;
          margin-top: 30px;
          margin-bottom: 40px;
        }
        .filter-btn {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 30px;
          color: var(--gray-300);
          padding: 10px 22px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          font-size: 13.5px;
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
        }
        .filter-btn:hover {
          border-color: rgba(0, 242, 254, 0.3);
          color: var(--white);
          background: rgba(255, 255, 255, 0.06);
          transform: translateY(-1px);
        }
        .filter-btn.active {
          background: linear-gradient(135deg, var(--phoenix-teal), rgba(0, 242, 254, 0.6));
          border-color: transparent;
          color: var(--white);
          box-shadow: 0 5px 15px rgba(0, 242, 254, 0.15);
        }
        .case-card.animate-fade {
          animation: fadeIn 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
        }
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(15px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .no-cases {
          grid-column: 1 / -1;
          text-align: center;
          padding: 60px 20px;
          color: var(--gray-400);
          font-size: 15px;
          background: rgba(255, 255, 255, 0.01);
          border: 1px dashed var(--glass-border);
          border-radius: 20px;
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
        }
      </style>

      <!-- 產業篩選 Tab 鍵 -->
      <div class="case-filters">
        <button class="filter-btn active" data-filter="all">全部案例</button>
        <button class="filter-btn" data-filter="manufacturing">製造與傳產</button>
        <button class="filter-btn" data-filter="medical">醫療與健康</button>
        <button class="filter-btn" data-filter="ecommerce">跨境電商</button>
        <button class="filter-btn" data-filter="professional">專業服務 (法務/會計)</button>
      </div>

      <!-- 動態載入容器 -->
      <div class="cases-grid" id="casesGridContainer" style="transition: opacity 0.2s ease;">
        <!-- JavaScript 會自動將卡片渲染至此 -->
      </div>
      
"""
    
    html = first_part + replacement_block + second_part
    
    # Now patch the scripts block before </body>
    closing_body = "</body>"
    if closing_body not in html:
        print("Error: </body> not found in index.html")
        return
        
    js_script = """  <!-- ─── 企業標竿案例動態載入與篩選 JS 邏輯 ─── -->
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      let allCases = [];
      const container = document.getElementById("casesGridContainer");
      const filterBtns = document.querySelectorAll(".filter-btn");

      // 格式化加粗文字
      const formatText = text => text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');

      // 1. 從 JSON 檔案動態抓取案例庫
      fetch("./cases/cases.json")
        .then(response => response.json())
        .then(data => {
          allCases = data;
          renderCases("all");
        })
        .catch(err => {
          console.error("無法載入案例庫:", err);
          container.innerHTML = `<div class="no-cases">無法載入案例庫，請檢查網路連線或稍後再試。</div>`;
        });

      // 2. 渲染卡片函數
      function renderCases(filter) {
        container.style.opacity = 0; // 漸隱動畫
        
        setTimeout(() => {
          container.innerHTML = "";
          const filteredCases = filter === "all" 
            ? allCases 
            : allCases.filter(c => c.industry === filter);

          if (filteredCases.length === 0) {
            container.innerHTML = `<div class="no-cases">此分類目前尚無公開範例，如需專屬產業簡報請對接顧問快診。</div>`;
            container.style.opacity = 1;
            return;
          }

          filteredCases.forEach(c => {
            const card = document.createElement("div");
            card.className = "case-card animate-fade";
            
            // 決定標籤顏色樣式
            let tagStyle = "";
            if (c.tag.includes("HR") || c.tag.includes("變革")) {
              tagStyle = 'style="color: var(--phoenix-gold); border-color: rgba(245, 166, 35, 0.25); background: rgba(245, 166, 35, 0.1);"';
            } else if (c.tag.includes("資安") || c.tag.includes("隱私") || c.tag.includes("合規")) {
              tagStyle = 'style="color: var(--phoenix-teal); border-color: rgba(0, 242, 254, 0.25); background: rgba(0, 242, 254, 0.1);"';
            } else {
              tagStyle = 'style="color: var(--phoenix-accent); border-color: rgba(233, 69, 96, 0.25); background: rgba(233, 69, 96, 0.1);"';
            }

            // 痛點與解法清單 HTML
            const painsHTML = c.pain_points.map(p => `<li class="case-list-item">${formatText(p)}</li>`).join("");
            const solsHTML = c.solutions.map(s => `<li class="case-list-item solution">${formatText(s)}</li>`).join("");
            const roiHTML = c.roi.map(r => `<li class="case-roi-item">${formatText(r)}</li>`).join("");

            card.innerHTML = `
              <div class="case-header">
                <div class="case-id-badges">
                  <span class="case-id">${c.id}</span>
                  <span class="case-tag" ${tagStyle}>${c.tag}</span>
                </div>
                <span class="case-tag" style="align-self: flex-start; margin-top: 4px; border-color: rgba(255,255,255,0.06); background: rgba(255,255,255,0.02); color: var(--gray-300);">${c.industry_name}</span>
                <h3 class="case-title">${c.title}</h3>
              </div>
              <div class="case-divider"></div>
              <div class="case-body">
                <div class="case-section">
                  <span class="case-section-title">🛑 業務痛點與挑戰</span>
                  <ul class="case-list">${painsHTML}</ul>
                </div>
                <div class="case-section">
                  <span class="case-section-title">⚡ 一線阻力與顧問解法</span>
                  <ul class="case-list">${solsHTML}</ul>
                </div>
                <div class="case-roi-box">
                  <span class="case-roi-title">📈 量化落地成效 (ROI)</span>
                  <ul class="case-roi-list">${roiHTML}</ul>
                </div>
              </div>
              <div class="case-footer">
                <div class="case-target-scheme">
                  <span class="scheme-label">對標建議方案</span>
                  <span class="scheme-value">${c.scheme}</span>
                </div>
                <a href="${c.detail_url}" target="_blank" class="case-btn">
                  🖥️ 閱讀完整規劃報告 (HTML) ➔
                </a>
              </div>
            `;
            container.appendChild(card);
          });
          
          container.style.opacity = 1; // 漸顯動畫
        }, 200);
      }

      // 3. Tab 切換事件綁定
      filterBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
          filterBtns.forEach(b => b.classList.remove("active"));
          e.target.classList.add("active");
          renderCases(e.target.getAttribute("data-filter"));
        });
      });
    });
  </script>
</body>"""
    
    html = html.replace(closing_body, js_script)
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Successfully patched index.html for dynamic B2B cases showcase!")

if __name__ == "__main__":
    patch_index()
