# -*- coding: utf-8 -*-
import openpyxl
import os

def check_excel_sheets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(base_dir, "curriculum", "unit_7_strategy", "phoenix_ai_canvas_4plus1.xlsx")
    
    if not os.path.exists(excel_path):
        print(f"Excel file not found at: {excel_path}")
        return
        
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    print("Sheets in phoenix_ai_canvas_4plus1.xlsx:")
    for idx, sheet in enumerate(wb.sheetnames):
        print(f"Sheet {idx+1}: {sheet}")
        
if __name__ == "__main__":
    check_excel_sheets()
