from pathlib import Path
import shutil
import pandas as pd

out_dir = Path('coffee_dataset_out')
src = out_dir / 'coffee_analytics_dataset.xlsx'
backup = out_dir / 'coffee_analytics_dataset.xlsx.corrupt'

if src.exists():
    try:
        shutil.move(str(src), str(backup))
        print('Backed up corrupt workbook to', backup)
    except Exception as e:
        print('Failed to back up existing workbook:', e)

# Read CSVs
files = {
    'dim_stores': out_dir / 'coffee_stores.csv',
    'dim_products': out_dir / 'coffee_products.csv',
    'dim_customers': out_dir / 'coffee_customers.csv',
    'dim_employees': out_dir / 'coffee_employees.csv',
    'fact_transactions': out_dir / 'coffee_transactions.csv',
    'fact_items': out_dir / 'coffee_transaction_items.csv',
}

dfs = {}
for sheet, path in files.items():
    if not path.exists():
        print('Missing CSV for', sheet, path)
        raise SystemExit(1)
    print('Reading', path.name)
    dfs[sheet] = pd.read_csv(path)

# Write a new Excel workbook using XlsxWriter (avoids openpyxl visibility bug)
try:
    with pd.ExcelWriter(src, engine='xlsxwriter') as writer:
        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    print('Recreated workbook at', src)
except Exception as e:
    print('Failed to write workbook:', e)
