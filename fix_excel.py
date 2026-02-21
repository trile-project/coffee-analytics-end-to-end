import openpyxl
from pathlib import Path
p = Path("coffee_dataset_out") / "coffee_analytics_dataset.xlsx"
print("Checking:", p.resolve())
try:
    wb = openpyxl.load_workbook(p)
    states = [(ws.title, ws.sheet_state) for ws in wb.worksheets]
    print("Sheet states:")
    for t,s in states:
        print(f"- {t}: {s}")
    if not any(s == 'visible' for _, s in states):
        wb.worksheets[0].sheet_state = 'visible'
        wb.save(p)
        print("Fixed: set first sheet to visible and saved the workbook.")
    else:
        print("No change needed; at least one sheet is visible.")
except Exception as e:
    print("Error while processing workbook:", type(e).__name__, e)
