Coffee Analytics End-to-End (120k+ Transactions)

End-to-end analytics portfolio project simulating a Starbucks-style retail coffee business.
This project demonstrates how raw transactional data can be generated, modeled, analyzed, and visualized using a modern analytics stack.

📌 Project Overview

This project covers the full analytics workflow:

Synthetic dataset generation (120k+ transactions)

Relational data modeling in MySQL

Analytical SQL (operations + customer analytics)

Excel pivot exploration

Power BI dashboard development

The goal is to showcase real business analytics scenarios including operational performance, customer segmentation, promotion effectiveness, and market basket analysis.

🧰 Tech Stack

Python — dataset generation

MySQL — schema design, data modeling, analytical SQL

Excel — exploratory pivot analysis

Power BI — dashboard & KPI reporting

📊 Dataset

Generated dataset includes:

120k+ transactions

250k+ line items

Stores

Customers

Products

Employees

⚠️ The full dataset is not committed due to file size.
Use the generator scripts to reproduce it locally.

▶️ How to Run
1️⃣ Generate Data

Run the main generator:

python project2.py

This creates:

CSV files

Excel dataset

Sample analytics outputs

⚠️ If Excel file fails to generate

Excel creation can fail due to memory limits or file locks.

Run recovery scripts:

python fix_excel.py
python recreate_excel.py

These scripts repair and regenerate the Excel dataset.

2️⃣ Load into MySQL

Run SQL scripts in this order:

Import CSV files using MySQL Workbench → Table Data Import Wizard

Then run:

createview_v_sales_line.sql

The view v_sales_line provides a BI-ready analytical table.

3️⃣ Run Analytics Queries

Execute:

Peak-hour staffing heatmap (store × hour).sql
RFM segmentation (window functions).sql
Promo uplift (baseline vs promo).sql
Market basket (top category pairs in same transaction).sql

This includes:

Peak hour operational analysis

RFM customer segmentation

Promotion uplift analysis

Market basket analysis

4️⃣ Power BI Dashboard

Run:

coffee_analytics.pbix

Dashboards include:

KPI overview

Peak hour heatmap

Store performance scatter plot

Customer segmentation

Promotion effectiveness

