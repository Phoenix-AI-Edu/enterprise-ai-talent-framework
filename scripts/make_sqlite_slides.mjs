import PptxGenJS from 'pptxgenjs';

const COLORS = {
  darkBg: '002B2B',
  primary: '006666',
  primaryLight: '4CA3A3',
  accent: 'FF7F50',
  accentLight: 'FFA07A',
  pale: 'F5FFFE',
  white: 'FFFFFF',
  black: '1B1B1B',
  gray: '888888',
  grayLight: 'E2F3F3',
};

const slideWidth = 13.33;
const slideHeight = 7.5;

function newOpt(opts = {}) {
  return { ...opts };
}

function addTitleSlide(pptx, title, subtitle) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.darkBg };

  slide.addText(title, {
    x: 0.7,
    y: 1.8,
    w: 11.6,
    h: 1.8,
    fontSize: 44,
    bold: true,
    fontFace: 'Georgia',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  });

  slide.addText(subtitle, newOpt({
    x: 0.7,
    y: 3.3,
    w: 11.0,
    h: 1.8,
    fontSize: 18,
    fontFace: 'Calibri',
    color: 'B9D9D9',
    align: 'left',
    valign: 'top',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.7,
    y: 5.0,
    w: 11.6,
    h: 0.15,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.7,
    y: 5.65,
    w: 11.6,
    h: 0.08,
    line: { type: 'none' },
    fill: { color: COLORS.primaryLight },
  }));

  return slide;
}

function addSectionSlide(pptx, section) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.primary };

  slide.addText(section, newOpt({
    x: 0.7,
    y: 2.6,
    w: 12.0,
    h: 2.0,
    fontSize: 40,
    bold: true,
    fontFace: 'Georgia',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.7,
    y: 4.5,
    w: 2.8,
    h: 0.18,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  return slide;
}

function addContentSlide(pptx, title, body, extra) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.white };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));

  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  if (extra && extra.accent) {
    slide.addShape(pptx.ShapeType.rect, newOpt({
      x: 12.55,
      y: 0.55,
      w: 0.55,
      h: 0.85,
      line: { type: 'none' },
      fill: { color: COLORS.accent },
    }));
  }

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.8,
    w: 1.1,
    h: 0.1,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  if (typeof body === 'string') {
    slide.addText(body, newOpt({
      x: 0.55,
      y: 2.15,
      w: 12.1,
      h: 4.4,
      fontSize: 16,
      fontFace: 'Calibri',
      color: COLORS.black,
      align: 'left',
      valign: 'top',
      lineSpacingMultiple: 1.35,
      bullet: { style: 'number', color: COLORS.primary },
      breakLine: true,
    }));
  } else if (Array.isArray(body)) {
    const textItems = [];
    body.forEach(b => {
      textItems.push({ text: b, options: newOpt({ fontSize: 16, fontFace: 'Calibri', bullet: true, breakLine: true }) });
    });
    slide.addText(textItems, newOpt({
      x: 0.55,
      y: 2.15,
      w: 12.1,
      h: 4.4,
      color: COLORS.black,
      align: 'left',
      valign: 'top',
      lineSpacingMultiple: 1.4,
    }));
  }

  return slide;
}

function addBulletSlide(pptx, title, bullets, note) {
  const textItems = bullets.map((line, i) => ({
    text: line,
    options: newOpt({ fontSize: 15, fontFace: 'Calibri', bullet: true, breakLine: true }),
  }));

  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.white };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));

  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.75,
    w: 1.1,
    h: 0.1,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  slide.addText(textItems, newOpt({
    x: 0.55,
    y: 2.15,
    w: 12.1,
    h: 4.4,
    color: COLORS.black,
    align: 'left',
    valign: 'top',
    lineSpacingMultiple: 1.45,
  }));

  if (note) slide.addNotes(note);

  return slide;
}

function addCodeSlide(pptx, title, code, note, lang) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.pale };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.darkBg },
  }));

  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.55,
    w: 1.8,
    h: 0.22,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));
  slide.addText(lang || 'Python', newOpt({
    x: 0.55,
    y: 1.55,
    w: 1.8,
    h: 0.22,
    fontSize: 13,
    bold: true,
    fontFace: 'Calibri',
    color: COLORS.white,
    align: 'center',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.95,
    w: 12.2,
    h: 4.65,
    line: { type: 'none' },
    fill: { color: '121A1A' },
  }));

  slide.addText(code, newOpt({
    x: 0.8,
    y: 1.05,
    w: 11.8,
    h: 4.85,
    fontSize: 15,
    fontFace: 'Consolas',
    color: 'B9FFEE',
    align: 'left',
    valign: 'top',
    lineSpacingMultiple: 1.2,
    breakLine: true,
  }));

  if (note) slide.addNotes(note);
  return slide;
}

function addTableSlide(pptx, title, headerTexts, plainRows, note) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.pale };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));
  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.55,
    w: 1.9,
    h: 0.22,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));
  slide.addText('比較表', newOpt({
    x: 0.55,
    y: 1.55,
    w: 1.9,
    h: 0.22,
    fontSize: 13,
    bold: true,
    fontFace: 'Calibri',
    color: COLORS.white,
    align: 'center',
    valign: 'middle',
  }));

  const allRows = [
    headerTexts.map(h => ({ text: h, options: newOpt({ fontSize: 15, bold: true, fontFace: 'Calibri', color: COLORS.black, align: 'center' }) })),
    ...plainRows.map(r => r.map(c => ({ text: c, options: newOpt({ fontSize: 14, fontFace: 'Calibri', color: COLORS.black, align: 'left' }) }))),
  ];

  slide.addTable(allRows, {
    x: 0.55,
    y: 1.95,
    w: 12.2,
    colW: [2.8, 3.1, 3.1, 3.2],
    border: { type: 'solid', pt: 0.5, color: 'C2DCD5' },
    rowH: [0.45, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58],
    fontFace: 'Calibri',
    fontSize: 14,
    align: 'left',
    valign: 'middle',
    rowSpacing: 'dbl',
  });

  if (note) slide.addNotes(note);
  return slide;
}

function addFlowSlide(pptx, title, steps) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.white };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));
  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  const boxW = 1.8;
  const boxH = 1.9;
  const y = 2.05;
  const gap = 0.65;
  const startX = 0.8;
  const shadowObj = { type: 'outer', blur: 4, offset: 3, angle: 45, opacity: 0.18, color: '000000' };

  steps.forEach((step, i) => {
    const x = startX + i * (boxW + gap);

    slide.addShape(pptx.ShapeType.rect, newOpt({
      x,
      y,
      w: boxW,
      h: boxH,
      line: { color: COLORS.primary, width: 2.5 },
      fill: { color: i % 2 === 0 ? COLORS.pale : COLORS.grayLight },
      shadow: shadowObj,
    }));

    slide.addText(step.title, newOpt({
      x,
      y: y + 0.12,
      w: boxW,
      h: 0.65,
      fontSize: 15,
      bold: true,
      fontFace: 'Calibri',
      color: COLORS.black,
      align: 'center',
      valign: 'middle',
    }));
    slide.addText(step.body, newOpt({
      x,
      y: y + 0.75,
      w: boxW,
      h: 1.05,
      fontSize: 13,
      fontFace: 'Calibri',
      color: COLORS.gray,
      align: 'center',
      valign: 'top',
      breakLine: true,
    }));

    if (i < steps.length - 1) {
      slide.addText('➜', newOpt({
        x: x + boxW + 0.02,
        y: y + 0.78,
        w: gap - 0.04,
        h: 0.5,
        fontSize: 36,
        color: COLORS.accent,
        align: 'center',
        valign: 'middle',
      }));
    }
  });

  return slide;
}

function addClosingSlide(pptx) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.darkBg };

  slide.addText('總結與後續學習路徑', newOpt({
    x: 0.7,
    y: 2.3,
    w: 12.0,
    h: 1.2,
    fontSize: 40,
    bold: true,
    fontFace: 'Georgia',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));
  slide.addText('謝謝聆聽，持續動手寫程式進步最快！', newOpt({
    x: 0.7,
    y: 3.7,
    w: 12.0,
    h: 1.0,
    fontSize: 20,
    fontFace: 'Calibri',
    color: 'B9D9D9',
    align: 'left',
    valign: 'top',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.7,
    y: 4.95,
    w: 12.0,
    h: 0.14,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  return slide;
}

function addTwoColumns(pptx, title, items) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.white };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));
  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));
  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.8,
    w: 1.1,
    h: 0.1,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  slide.addText(items.left.title, newOpt({
    x: 0.55,
    y: 2.2,
    w: 5.8,
    h: 0.55,
    fontSize: 18,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.primary,
    align: 'left',
    valign: 'middle',
  }));
  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 2.70,
    w: 5.8,
    h: 0.07,
    line: { type: 'none' },
    fill: { color: COLORS.accentLight },
  }));

  const leftItems = items.left.rows.map(line => ({
    text: line,
    options: newOpt({ fontSize: 15, fontFace: 'Calibri', bullet: true, breakLine: true }),
  }));
  slide.addText(leftItems, newOpt({
    x: 0.55,
    y: 2.95,
    w: 5.8,
    h: 3.85,
    color: COLORS.black,
    align: 'left',
    valign: 'top',
    lineSpacingMultiple: 1.4,
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 7.05,
    y: 2.05,
    w: 0.04,
    h: 4.8,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));

  slide.addText(items.right.title, newOpt({
    x: 7.3,
    y: 2.2,
    w: 5.4,
    h: 0.55,
    fontSize: 18,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.primary,
    align: 'left',
    valign: 'middle',
  }));
  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 7.3,
    y: 2.70,
    w: 5.4,
    h: 0.07,
    line: { type: 'none' },
    fill: { color: COLORS.accentLight },
  }));

  const rightItems = items.right.rows.map(line => ({
    text: line,
    options: newOpt({ fontSize: 15, fontFace: 'Calibri', bullet: true, breakLine: true }),
  }));
  slide.addText(rightItems, newOpt({
    x: 7.3,
    y: 2.95,
    w: 5.4,
    h: 3.85,
    color: COLORS.black,
    align: 'left',
    valign: 'top',
    lineSpacingMultiple: 1.4,
  }));

  return slide;
}

function addChecklistSlide(pptx, title, items) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.pale };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.accent },
  }));
  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));
  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0.55,
    y: 1.95,
    w: 1.1,
    h: 0.1,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));

  const textItems = items.map(line => ({
    text: line,
    options: newOpt({ fontSize: 16, fontFace: 'Calibri', bullet: true, breakLine: true }),
  }));
  slide.addText(textItems, newOpt({
    x: 0.55,
    y: 2.3,
    w: 12.1,
    h: 4.4,
    color: COLORS.black,
    align: 'left',
    valign: 'top',
    lineSpacingMultiple: 1.5,
  }));

  return slide;
}

function addSmallHighlightSlide(pptx, title, highlightText, note) {
  const slide = pptx.addSlide();
  slide.width = slideWidth;
  slide.height = slideHeight;
  slide.background = { color: COLORS.white };

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 0,
    y: -0.1,
    w: 13.8,
    h: 4.9,
    line: { type: 'none' },
    fill: { color: COLORS.primary },
  }));
  slide.addText(title, newOpt({
    x: 0.55,
    y: 0.45,
    w: 12.3,
    h: 1.05,
    fontSize: 36,
    bold: true,
    fontFace: 'Arial Black',
    color: COLORS.white,
    align: 'left',
    valign: 'middle',
  }));

  slide.addShape(pptx.ShapeType.rect, newOpt({
    x: 1.05,
    y: 3.05,
    w: 11.23,
    h: 1.85,
    line: { type: 'none' },
    fill: { color: COLORS.accentLight },
  }));

  slide.addText(highlightText, newOpt({
    x: 1.25,
    y: 3.2,
    w: 10.85,
    h: 1.55,
    fontSize: 20,
    bold: true,
    fontFace: 'Georgia',
    color: COLORS.darkBg,
    align: 'center',
    valign: 'middle',
  }));

  if (note) slide.addNotes(note);
  return slide;
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'AI Talent';
pptx.title = 'Python SQLite3 程式小白教學投影片';
pptx.subject = 'SQLite3 入門實作教學';

addTitleSlide(pptx, 'Python SQLite3 程式小白教學', '從資料庫基礎到實戰 CRUD，一頁上手最輕量的資料庫');
addSectionSlide(pptx, '課程大綱與學習目標');
addBulletSlide(pptx, '課程大綱', [
  '認識資料庫基本概念與 SQLite 定位',
  'SQLite 安裝與環境設定',
  '連線與Cursor基本操作',
  'CREATE/INSERT/READ/UPDATE/DELETE 全流程',
  '查詢強化：fetchone/fetchall/fetchmany',
  '參數化查詢與 SQL 注入防禦',
  '主鍵、AUTOINCREMENT與資料類型',
  '實作案例、除錯技巧、學習路徑',
]);

addTwoColumns(pptx, '為什麼從 SQLite 開始？', {
  left: {
    title: '新手友善',
    rows: [
      '內建於 Python，不需額外安裝伺服器',
      '單一檔案即可備份與攜帶',
      '語法接近業界主流資料庫',
      '適合練習 SQL 與資料庫邏輯',
    ],
  },
  right: {
    title: '讓我閃耀',
    rows: [
      '零組態起步，專注學習概念',
      '手機到伺服器都能執行',
      '從小專案到原型都適用',
      '再進階 MySQL/PostgreSQL 很容易',
    ],
  },
});

addContentSlide(pptx, '為什麼學 SQLite？', [
  'SQLite 是目前最廣泛部署的資料庫，Android、iOS、macOS、Chrome 與無數桌面軟體都內建使用。',
  '小白起步的最佳選擇：不需要安裝資料庫伺服器、不需要帳號密碼設定、不需要背景服務。',
  '學習 SQLite 的概念可無縫遷移到 MySQL、PostgreSQL 等大型資料庫。',
  '你只需要會 Python，就能開始操作資料庫。',
], { accent: true });

addSectionSlide(pptx, '資料庫基礎概念');
addContentSlide(pptx, '資料庫是什麼？', [
  '資料庫（Database）是用來長期結構化管理資料的系統。',
  '你可以把它想成「具備查詢能力的 Excel 儲存區」。',
  '資料庫會把資料分成多個表格，每張表格有欄位名稱與資料型別。',
  '表格內容由一或多個欄位組成主鍵（Primary Key），唯一代表每一列記錄。',
  '常見的資料庫伺服器：MySQL、PostgreSQL、MSSQL、SQLite。',
]);

addFlowSlide(pptx, '資料庫核心元件流程', [
  { title: 'Database', body: '一個 .db 檔案或資料庫服務實例' },
  { title: 'Table', body: '同類資料的表格，例如 users、orders' },
  { title: 'Column', body: '儲存特定屬性，例如 id、name、price' },
  { title: 'Row', body: '一筆紀錄，例如一筆使用者資料' },
]);

addBulletSlide(pptx, '常用資料庫比較：SQLite vs MySQL vs PostgreSQL', [
  'SQLite：輕量、單檔、內建、適合嵌入裝置與小型應用。',
  'MySQL：客戶端/伺服器架構，適合網站與多人連線。',
  'PostgreSQL：功能最完整，適合複雜分析、GIS、擴充型別。',
  'SQLite 不支援使用者帳號、外部連線與儲存程序。',
  'MySQL / PostgreSQL 需要安裝與管理後台服務。',
  '初學者先學 SQLite，最省時間、最少挫折。',
]);

addTableSlide(pptx, '三大資料庫功能比較', [
  '規格',
  'SQLite',
  'MySQL',
  'PostgreSQL',
], [
  ['檔案型態', '單一檔案', '伺服器', '伺服器'],
  ['設定難度', '極低', '中等', '較高'],
  ['最大資料量', '約 140 TB', '視版本', '超大'],
  ['併發讀寫', '有限', '強大', '強大'],
  ['應用場景', '手機/桌面/嵌入式', '網站', '企業/分析'],
]);

addSectionSlide(pptx, '安裝與環境設定');
addContentSlide(pptx, 'SQLite 環境：Python 內建', [
  'SQLite3 是 Python 標準函式庫，PYTHON 3.x 不需要額外安裝。',
  '只要你的 Python 可以 import sqlite3，就已經準備好了。',
  '建議在終端機執行：python -c "import sqlite3; print(sqlite3.sqlite_version)"',
  '編寫程式的編輯器建議：VS Code、PyCharm、Thonny。',
  '建議 Python 版本：3.9 以上，較新版本有更好的型別提示支援。',
]);

addCodeSlide(pptx, '範例：驗證 SQLite3 版本', `import sqlite3

print("你的 Python 版本可用")
print("SQLite 版本：", sqlite3.sqlite_version)

# 成功執行表示連線核心模組已可用`, '這張投影片展示如何只用一行確認本機 SQLite3 環境正常。');

addBulletSlide(pptx, '安裝確認要點', [
  '確認 python3 指令是否存在。',
  '確認 import sqlite3 不會报错。',
  'SQLite 並不需要額外伺服器。',
  'Windows 與 macOS/Linux 行為一致。',
]);

addSectionSlide(pptx, '資料庫連線與關閉');
addContentSlide(pptx, '建立連線的意義', [
  '資料庫連線就像是你和資料庫檔案之間的對話管道。',
  '用 connect() 開啟管道，成功後會回傳 Connection 物件。',
  '你可以用它執行查詢、管理交易、關閉連線、備份檔案。',
  '不使用時要呼叫 close()，避免檔案鎖定與資源浪費。',
]);

addCodeSlide(pptx, '基礎連線與關閉', `import sqlite3

connection = sqlite3.connect("school.db")
print("連線成功")

cursor = connection.cursor()
print("Cursor 建立成功")

cursor.close()
connection.close()
print("連線已關閉")`, '重點在 connect()、cursor()、close() 三步驟。');

addTwoColumns(pptx, '常見錯誤與解法', {
  left: {
    title: '錯誤訊息',
    rows: [
      'OperationalError: database is locked',
      'ProgrammingError: Incorrect number of bindings',
      'FileNotFoundError：缺少 .db 路徑',
    ],
  },
  right: {
    title: '建議解法',
    rows: [
      '另一個程式正在使用資料庫，關閉後重試',
      'question mark 數量要和資料筆數一致',
      'connect() 會自動建立檔案，但目錄必須存在',
    ],
  },
});

addSectionSlide(pptx, 'Create / Insert：寫入資料');
addContentSlide(pptx, '建立資料表 CREATE TABLE', [
  '建立資料表前要先定義欄位、型別、長度與主鍵。',
  'SQLite 的型別親和性較寬鬆：TEXT、INTEGER、REAL、BLOB、NULL。',
  'PRIMARY KEY 常見搭配 INTEGER AUTOINCREMENT。',
  'VARCHAR(255) 寫法可運作，但更像是「親和型別」而非嚴格限制。',
  '建立資料表時應避免大小寫不一致造成管理困擾。',
]);

addCodeSlide(pptx, '建立 students 資料表', `import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute(\`\`\`
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT
)
\`\`\`)

connection.commit()
cursor.close()
connection.close()

print("資料表建立完畢")`, '使用 IF NOT EXISTS 可避免重複執行建立指令。');

addBulletSlide(pptx, '欄位型別常用選擇', [
  'INTEGER：整數，適合年齡、數量、數量、主鍵。',
  'REAL：小數、價格、測量值。',
  'TEXT：姓名、地址、敘述。',
  'BLOB：圖片、檔案二進位內容。',
  'DATE / DATETIME：SQLite 仍用 TEXT/INTEGER/REAL 存，應用層處理格式。',
]);

addSectionSlide(pptx, 'CRUD：Read / Update / Delete');
addContentSlide(pptx, '讀取資料 SELECT', [
  'SELECT 搭配 FROM、WHERE、ORDER BY 就能讀取資料。',
  'fetchone() 只讀一筆，適合確認為唯一資料時使用。',
  'fetchall() 回傳整個結果清單，資料量大時注意記憶體。',
  'fetchmany(size) 回傳一批，適合批次處理或分頁。',
  'row_factory = sqlite3.Row 可讓回傳結果像字典操作。',
]);

addCodeSlide(pptx, '新增與查詢兩段範例', `import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()


# 新增
cursor.execute(
    "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
    ("Amy", 18, "Taipei")
)
connection.commit()


# 查詢全部
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(row)


# 查詢一筆
cursor.execute("SELECT * FROM students WHERE id = ?", (1,))
print(cursor.fetchone())

cursor.close()
connection.close()`, '範例涵蓋 INSERT、fetchall、fetchone。');

addBulletSlide(pptx, 'cursor.execute() 使用重點', [
  '第一個參數是 SQL，可用參數化 ? 或命名參數 :name。',
  '第二個參數如果是 tuple/list/dict，會綁定到參數位置。',
  '避免用字串拼接 SQL，尤其在處理使用者輸入時。',
  ' executemany() 適合批次大量寫入。',
]);

addChecklistSlide(pptx, '互動練習：成功讀到資料了嗎？', [
  '請開啟 school.db',
  '請新增 2 位學生姓名：Alice、Bob',
  '請把所有學生的名字印出',
  '請用 fetchone() 找 id = 1 的學生',
  '請手動關閉連線並觀察檔案內容',
]);

addSectionSlide(pptx, '進階查詢與修改');
addContentSlide(pptx, 'Update / Delete 與條件', [
  'UPDATE 要搭配 WHERE 才會更新指定範圍，否則全部都會被改掉。',
  'DELETE 的風險更大，無條件只刪帶條件的紀錄。',
  '預習 transaction 概念：commit() 才會真正寫入，rollback() 可撤銷未 commit。',
  '建議每次更新後 SELECT 確認結果與預期一致。',
]);

addCodeSlide(pptx, 'Update 與 Delete 合併範例', `import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

# Update
cursor.execute(
    "UPDATE students SET city = ? WHERE name = ?",
    ("Kaohsiung", "Amy")
)

# Delete
cursor.execute("DELETE FROM students WHERE age < ?", (16,))

connection.commit()
print("更新與刪除完成")

cursor.close()
connection.close()`, '實務常用更新與刪除，一定要搭配 WHERE。');

addTwoColumns(pptx, 'fetch 差異速查', {
  left: {
    title: 'fetchone()',
    rows: [
      '只讀取一筆紀錄',
      '回傳 tuple 或 None',
      '適合單筆查詢',
      '游標會前進到下一個',
    ],
  },
  right: {
    title: 'fetchall()',
    rows: [
      '讀取所有剩餘紀錄',
      '回傳 list[tuple]',
      '資料量大時注意效能',
      '可用 for row in rows 遍歷',
    ],
  },
});

addBulletSlide(pptx, 'executemany() 概念', [
  'executemany(sql, seq_of_parameters) 做批次操作。',
  '適合一次插入大量資料、批次更新規則明確的資料。',
  'SEQ 的每一筆都會被重複執行一次 SQL。',
  '語法範例：executemany(\n    "INSERT INTO t(name, age) VALUES (?, ?)",\n    data_list\n)',
]);

addSectionSlide(pptx, '參數化查詢與安全');
addContentSlide(pptx, '為什麼要參數化？', [
  '資料庫驅動程式會把 ? 對應的參數當資料，而不是可執行的 SQL。',
  '這樣使用者輸入就不會被誤判成指令，避免 SQL Injection。',
  '命名參數 :name 適合多參數語意清晰時使用。',
  '常被攻擊的按鈕：搜尋框、登入欄位、URL 參數。',
]);

addBulletSlide(pptx, 'SQL Injection 概念', [
  '攻擊者輸入：任意字串如 admin\' OR 1=1 --',
  '若直接拼字串，資料庫會誤以為是額外條件或註解解除限制。',
  '參數化查詢讓使用者輸入永遠只被當資料，不會變成 SQL 片段。',
  '永遠不要用 + 或 format() 拼接使用者輸入進 SQL。',
]);

addCodeSlide(pptx, '? 參數化查詢範例', `import sqlite3

city = input("輸入要查詢的城市：")
# 下面這行使用參數化查詢，避免 SQL injection
cursor.execute(
    "SELECT * FROM students WHERE city = ?",
    (city,)
)
rows = cursor.fetchall()
print("找到", len(rows), "筆")`, '重點：第二個參數即使是單一值，也要是 tuple。');

addCodeSlide(pptx, 'named style 與 row_factory 組合', `import sqlite3

connection = sqlite3.connect("school.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute(
    "SELECT id, name, age FROM students WHERE age >= :min_age",
    {"min_age": 18}
)
rows = cursor.fetchall()

for row in rows:
    print("id：", row["id"])
    print("name：", row["name"])
    print("age：", row["age"])

cursor.close()
connection.close()`, 'row_factory 讓每一筆資料可以用 key 取值，更易維護。');

addBulletSlide(pptx, '參數化小提醒', [
  '? 參數用 tuple，即使只有一個值也要加逗號。',
  ':name 命名參數可用 dict 綁定。',
  '參數化查詢衡量原則：所有來自使用者輸入都應參數化。',
  '資料庫驅動會自動型別轉換，不需要自行處理。',
]);

addSectionSlide(pptx, '型別、主鍵與交易');
addContentSlide(pptx, 'SQLite 的類型親和性', [
  'SQLite 儲存型別只分成：NULL、INTEGER、REAL、TEXT、BLOB。',
  '欄位聲明型別更像提示，不是嚴格約束。',
  '例如声明 INTEGER，放文字也能存入，只是會嘗試轉換。',
  '寫給程式閱讀時，欄位聲明仍建議正確。',
]);

addContentSlide(pptx, '主鍵與 AUTOINCREMENT', [
  'PRIMARY KEY 在 SQLite 內建 rowid，接近一本書的頁碼。',
  'AUTOINCREMENT 只是保證 rowid 不會重複使用。',
  '大多數時候不需要 AUTOINCREMENT，直接 INTEGER PRIMARY KEY 即可。',
  '刪除資料後，rowid 不會主動補回空缺。',
]);

addBulletSlide(pptx, '交易與 commit/rollback', [
  '每次 execute() 不會立刻寫入檔案，直到呼叫 commit()。',
  '發生錯誤時可呼叫 rollback() 回到之前的狀態。',
  '好習慣：寫完邏輯才一次 commit，保持資料一致性。',
  '使用 with 資料庫連線可自動管理交易，減少錯誤。',
]);

addCodeSlide(pptx, 'with 連線自動處理', `import sqlite3

with sqlite3.connect("school.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
        ("Carol", 17, "Tainan")
    )
    cursor.execute(
        "UPDATE students SET city = 'Hsinchu' WHERE name = ?",
        ("Carol",)
    )

# 離開 with 區塊會自動 commit
# 發生例外則自動 rollback
print("完成")`, '使用 with 可減少忘記 commit 或 close 的機會。');

addSectionSlide(pptx, '常見錯誤與 Debug 技巧');
addContentSlide(pptx, '常見錯誤總覽', [
  '資料庫被鎖定：確認無其他程式開啟，並使用 with 管理連線。',
  'SQL 語法錯誤：先去 SQLite shell 或線上工具確認語法。',
  '參數數量錯誤：? 的數量 != tuple/list 的長度。',
  '遺忘 commit：修改不會真正寫入。',
  '路徑錯誤：資料夾不存在時 connect 仍不會自動建立目錄。',
]);

addBulletSlide(pptx, 'Debug 檢查清單', [
  '先印出 cursor.execute 的 SQL 與參數內容',
  '改用 VERY SIMPLE SQL 單獨測試',
  '確認資料庫檔案路徑是否正確',
  '中斷程式前先查看 school.db 是否被鎖定',
  '使用 try/except 捕捉錯誤並印出差異',
]);

addCodeSlide(pptx, '除錯範例：try/except 包裝', `import sqlite3

try:
    connection = sqlite3.connect("school.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
        ("Dave",),  # 故意少參數
    )
    connection.commit()
except sqlite3.Error as e:
    print("資料庫錯誤：", e)
finally:
    cursor.close()
    connection.close()`, 'error handling 能讓你快速看到失敗原因。');

addSmallHighlightSlide(pptx, '互動提醒：今天就動手寫 10 行程式碼', '重複練習 connect、cursor、execute、commit、close，才會真的內化。');

addChecklistSlide(pptx, '課後練習清單（Day 1）', [
  '完成 students 資料表，並新增 3 筆學生資料',
  '用 SELECT * 印出全部學生資料',
  '用 fetchone() 取得一位學生',
  '變更一位學生的城市並重新查詢',
  '刪除年齡最小的一筆資料',
]);

addBulletSlide(pptx, '後續學習路徑', [
  ' mastered SQLite insert/select/update/delete 之後，可學 JOIN 與子查詢。',
  '一律使用參數化查詢，直到成為習慣。',
  '進階可學 ORM 工具如 SQLAlchemy Core 或 peewee。',
  '再往上可學 MySQL、PostgreSQL，理解索引、交易隔離層級。',
  '持續做小專案：記帳本、閱讀清單、個人履歷查詢系統。',
]);

addBulletSlide(pptx, '參考資源', [
  'Python 官方文件：sqlite3 — DB-API 2.0 interface for SQLite databases',
  'SQLite 官方文件：https://www.sqlite.org/docs.html',
  'W3Schools SQL Tutorial / Mode SQL Tutorial',
  '推荐的练手项目：sample-database/crm、todo list with persistence',
]);

addClosingSlide(pptx);

const outDir = 'C:/Users/m1016/Documents/AI_Talent';
const outFile = outDir + '/python_sqlite3_tutorial.pptx';
pptx.writeFile({ fileName: outFile })
  .then(() => {
    console.log('OUTPUT=' + outFile);
  })
  .catch(err => {
    console.error('生成失敗', err);
    process.exit(1);
  });
