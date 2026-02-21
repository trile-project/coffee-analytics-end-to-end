# Coffee Analytics End-to-End Platform
**Retail Coffee Business Simulation — 120k+ Transactions**

An end-to-end analytics portfolio project that simulates a Starbucks-style retail coffee business.  
This project demonstrates how transactional data can be generated, modeled, analyzed, and visualized using a modern analytics stack.

---

## Overview

This project showcases the complete analytics lifecycle — from synthetic data generation to business intelligence reporting.

Key objectives:

- Simulate production-scale retail transaction data  
- Design a relational analytical data model  
- Perform operational and customer analytics using SQL  
- Conduct exploratory analysis in Excel  
- Deliver executive-level dashboards in Power BI  

The project focuses on realistic business scenarios including operational performance, customer segmentation, promotion effectiveness, and market basket analysis.

---

## Tech Stack

- Python — synthetic dataset generation  
- MySQL — schema design, data modeling, analytical SQL  
- Excel — exploratory analysis and pivot validation  
- Power BI — dashboarding, KPI reporting, storytelling  

---

## Dataset

The generated dataset represents a multi-store retail coffee environment and includes:

- 120k+ transactions  
- 250k+ line items  
- Stores  
- Customers  
- Products  
- Employees  

Note: The dataset is not committed due to file size.  
Use generator scripts to reproduce locally.

---

## Project Structure


/sql
/data
/scripts
/powerbi
README.md


---

## How to Run

### 1. Generate Data

Run:


python project2.py


Outputs:

- CSV datasets  
- Excel dataset  
- Sample analytics outputs  

If Excel generation fails:


python fix_excel.py
python recreate_excel.py


---

### 2. Load into MySQL

Run SQL scripts in order:

- sql/00_create_database.sql  
- sql/01_create_tables.sql  

Import CSV files using MySQL Workbench → Table Data Import Wizard.

Then run:

- sql/03_views.sql  

The view `v_sales_line` provides a BI-ready analytical table.

---

### 3. Run Analytics

Execute:

- sql/04_advanced_analysis.sql  

Includes:

- Peak hour analysis  
- Store performance  
- RFM segmentation  
- Promotion uplift  
- Market basket analysis  

---

### 4. Power BI Dashboard

Open:


powerbi/coffee_analytics.pbix


Dashboards include:

- KPI overview  
- Peak hour heatmap  
- Store performance visualization  
- Customer segmentation  
- Promotion effectiveness  

---

## Business Value

This project demonstrates:

- End-to-end analytics workflow  
- Production-style SQL analytics  
- Data modeling for BI  
- Retail operations insights  
- Customer analytics  
- Executive dashboard design  

---

## Notes

This portfolio project simulates real analytics workflows used in retail and supply chain environments.
