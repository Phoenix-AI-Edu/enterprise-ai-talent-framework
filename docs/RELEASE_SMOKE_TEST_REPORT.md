# Release Smoke Test Report (Phase E1)

## 1. cases.json / cases_data.js Validation
- **cases.json**: Valid JSON
- **cases_data.js**: All 24 `detail_url` targets exist.

## 2. Missing Files Check
- No required files are missing.

## 3. Dead Links Check
- Dead links detected:
  - `cases\html\manufacturing_04_electroplate_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_12_okayama_sbir_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_06_ai_visual_inspection.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_16_okayama_filter.html` -> `../index.html#cases`
  - `cases\html\manufacturing_11_okayama_forge_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_08_henda_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_07_dingsheng_voice_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_09_luzhu_coldheading_ai.html` -> `../index.html#cases`
  - `cases\html\retail_03_yuepin_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_05_sbir_ready_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_10_okayama_fastener_ai.html` -> `../index.html#cases`
  - `cases\html\finance_01_dingtai_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_14_okayama_barcode.html` -> `../index.html#cases`
  - `cases\html\manufacturing_13_okayama_heat_treatment.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_12_okayama_sbir_ai.html` -> `./index.html#pricing`
  - `cases\html\retail_02_mingchadao_tea_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_16_okayama_filter.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_15_okayama_cbam.html` -> `../index.html#cases`
  - `cases\html\manufacturing_04_electroplate_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_09_luzhu_coldheading_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_05_sbir_ready_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_10_okayama_fastener_ai.html` -> `./index.html#pricing`
  - `cases\html\finance_01_dingtai_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_06_ai_visual_inspection.html` -> `../index.html#cases`
  - `cases\html\manufacturing_14_okayama_barcode.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_08_henda_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_11_okayama_forge_ai.html` -> `../index.html#cases`
  - `cases\html\retail_03_yuepin_ai.html` -> `../index.html#cases`
  - `cases\html\manufacturing_07_dingsheng_voice_ai.html` -> `../index.html#cases`
  - `cases\html\retail_02_mingchadao_tea_ai.html` -> `./index.html#pricing`
  - `cases\html\manufacturing_13_okayama_heat_treatment.html` -> `../index.html#cases`
  - `cases\html\manufacturing_15_okayama_cbam.html` -> `./index.html#pricing`

## 4. Form Links
- Found form link in `index.html`: https://docs.google.com/forms/d/e/1FAIpQLSfGlE4m-Tgg2AXcIGRy90jNuroTnt8ZGwB8r0E35msJIPw_xA/viewform
- Found form link in `experience\central-kitchen-ai-agent\index.html`: https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform
- Found form link in `index.html`: https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform

## 5. Privacy Links
- Found privacy link in `index.html`: ./privacy.html
- Found privacy link in `experience\central-kitchen-ai-agent\index.html`: ../../privacy.html
- Found privacy link in `experience\index.html`: ../privacy.html
