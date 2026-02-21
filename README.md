**# Coffee Analytics End-to-End (120k+ Transactions)

End-to-end analytics portfolio project based on a Starbucks-like coffee shop dataset.

## Tech Stack
- Python (data generation)
- MySQL (schema, views, advanced SQL analytics)
- Excel (pivot analysis)
- Power BI (dashboard + KPI reporting)

## Dataset
Generated dataset includes:
- 120k transactions
- 250k+ line items
- stores, customers, products, employees

Full dataset is not committed to GitHub.
Use the generator script to reproduce it.

## How to Run
### 1) Generate data
```run project2.py

# if coffee_analytics_dataset fail to create -----> run fix_excel.py and recreate_excel.py

###2) Load into MySQL

Run SQL scripts in this order:

sql/00_create_database.sql

sql/01_create_tables.sql

Import CSVs using Workbench Wizard

sql/03_views.sql

3) Analytics

Run:

sql/04_advanced_analysis.sql

4) Power BI Dashboard

See powerbi/dashboard_instructions.md

Key Analyses

Peak-hour staffing heatmap (store × hour)

RFM customer segmentation

Promotion uplift vs baseline AOV

Market basket (category pairs)**********
