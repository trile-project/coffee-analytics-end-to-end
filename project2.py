import numpy as np
import pandas as pd
from pathlib import Path

# ---------- CONFIG ----------
N_TRANSACTIONS = 120_000        # 100k+
SEED = 42
OUT_DIR = Path("coffee_dataset_out")

START = pd.Timestamp("2025-01-01")
END   = pd.Timestamp("2025-12-31 23:59:59")

# ---------- SETUP ----------
np.random.seed(SEED)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- DIM: STORES ----------
n_stores = 35
cities = ["Seattle","Bellevue","Redmond","Tacoma","Everett","Kirkland","Renton","Bothell","Issaquah","Olympia"]
store_types = ["Urban","Suburban","Drive-Thru","Campus","Airport","Grocery Kiosk"]
regions = ["PNW-North","PNW-Central","PNW-South"]

stores = pd.DataFrame({
    "store_id": [f"S{str(i).zfill(3)}" for i in range(1, n_stores+1)],
    "store_name": [f"BeanBrew #{i:03d}" for i in range(1, n_stores+1)],
    "city": np.random.choice(cities, n_stores),
    "region": np.random.choice(regions, n_stores, p=[0.35,0.40,0.25]),
    "store_type": np.random.choice(store_types, n_stores, p=[0.35,0.30,0.20,0.10,0.03,0.02]),
    "open_date": pd.to_datetime(np.random.choice(pd.date_range("2014-01-01","2024-12-31"), n_stores)).date
})

# ---------- DIM: PRODUCTS ----------
categories = ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé","Bakery","Sandwich","Snack","Merch"]
base_price_map = {
    "Brewed Coffee": (2.25, 4.75),
    "Espresso":      (3.25, 6.75),
    "Cold Brew":     (3.75, 6.95),
    "Tea":           (2.95, 6.25),
    "Frappé":        (4.25, 7.45),
    "Bakery":        (2.25, 5.95),
    "Sandwich":      (4.95, 9.95),
    "Snack":         (1.25, 4.95),
    "Merch":         (6.95, 29.95)
}

n_products = 120
product_category = np.random.choice(categories, n_products, p=[0.14,0.18,0.10,0.10,0.06,0.16,0.10,0.10,0.06])

def make_name(cat):
    if cat in ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"]:
        flavor = np.random.choice(["House","Mocha","Vanilla","Caramel","Hazelnut","Matcha","Chai","Toffee","Cinnamon","Pumpkin"])
        style  = np.random.choice(["Latte","Americano","Cappuccino","Macchiato","Mocha","Brew","Nitro","Refresher","Tea","Frap"])
        return f"{flavor} {style}"
    if cat == "Bakery":
        return np.random.choice(["Croissant","Blueberry Muffin","Banana Bread","Cinnamon Roll","Scone","Cookie","Brownie","Cake Pop"])
    if cat == "Sandwich":
        return np.random.choice(["Turkey & Swiss","Bacon Gouda","Egg & Cheddar","Ham & Cheese","Veggie Wrap","Chicken Panini"])
    if cat == "Snack":
        return np.random.choice(["Chips","Protein Bar","Trail Mix","Fruit Cup","Yogurt","Jerky"])
    return np.random.choice(["Tumbler","Mug","Beans 12oz","Beans 2lb","Gift Card","Sticker Pack","French Press"])

names = [make_name(c) for c in product_category]
prices, cogs = [], []
for cat in product_category:
    lo, hi = base_price_map[cat]
    p = np.round(np.random.uniform(lo, hi), 2)
    prices.append(p)
    c = p * np.random.uniform(0.22, 0.55) if cat != "Merch" else p * np.random.uniform(0.45, 0.70)
    cogs.append(np.round(c, 2))

products = pd.DataFrame({
    "product_id": [f"P{str(i).zfill(4)}" for i in range(1, n_products+1)],
    "product_name": names,
    "category": product_category,
    "default_unit_price": prices,
    "unit_cogs": cogs,
    "is_seasonal": np.random.choice([0,1], n_products, p=[0.85,0.15])
}).drop_duplicates(subset=["product_name","category"]).reset_index(drop=True)
products["product_id"] = [f"P{str(i).zfill(4)}" for i in range(1, len(products)+1)]

# ---------- DIM: CUSTOMERS ----------
n_customers = 42_000
first_names = ["Alex","Sam","Jordan","Taylor","Morgan","Casey","Riley","Jamie","Avery","Cameron","Parker","Quinn","Skyler","Reese","Rowan"]
last_names  = ["Lee","Nguyen","Patel","Garcia","Smith","Johnson","Brown","Davis","Wilson","Martinez","Anderson","Thomas","Jackson","White","Harris"]
domains     = ["gmail.com","yahoo.com","outlook.com","icloud.com","hotmail.com"]

def rand_phone(n):
    a = np.random.randint(200,999,n)
    b = np.random.randint(200,999,n)
    c = np.random.randint(1000,9999,n)
    return [f"{a[i]}-{b[i]}-{c[i]}" for i in range(n)]

customers = pd.DataFrame({
    "customer_id": [f"C{str(i).zfill(6)}" for i in range(1, n_customers+1)],
    "first_name": np.random.choice(first_names, n_customers),
    "last_name":  np.random.choice(last_names, n_customers),
    "phone": rand_phone(n_customers),
    "loyalty_tier": np.random.choice(["None","Green","Gold","Platinum"], n_customers, p=[0.35,0.35,0.22,0.08]),
    "signup_date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01","2025-12-31"), n_customers)).date,
    "marketing_opt_in": np.random.choice([0,1], n_customers, p=[0.45,0.55]),
})
customers["email"] = (
    customers["first_name"].str.lower() + "." +
    customers["last_name"].str.lower() +
    np.random.randint(1,9999,n_customers).astype(str) + "@" +
    np.random.choice(domains, n_customers)
)

# ---------- DIM: EMPLOYEES ----------
n_employees = 420
employees = pd.DataFrame({
    "employee_id": [f"E{str(i).zfill(5)}" for i in range(1, n_employees+1)],
    "store_id": np.random.choice(stores["store_id"], n_employees),
    "role": np.random.choice(["Barista","Shift Supervisor","Cashier"], n_employees, p=[0.72,0.18,0.10]),
    "hire_date": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01","2025-12-31"), n_employees)).date,
    "hourly_rate": np.round(np.random.uniform(17.5, 27.5, n_employees), 2)
})

# ---------- FACT: TRANSACTIONS (VECTOR WEIGHTED TIME) ----------
all_days = pd.date_range(START.date(), END.date(), freq="D")
dow_weights = np.array([1.02,1.04,1.05,1.06,1.10,0.92,0.88])
dow_weights = dow_weights / dow_weights.sum()
day_probs = dow_weights[all_days.dayofweek.values]
day_probs = day_probs / day_probs.sum()
sampled_days = np.random.choice(all_days, N_TRANSACTIONS, p=day_probs)

hours = np.arange(5, 22)
hour_weights = np.array([0.02,0.03,0.05,0.08,0.10,0.11,0.10,0.08,0.06,0.05,0.04,0.04,0.05,0.06,0.05,0.04,0.03])
hour_weights = hour_weights / hour_weights.sum()
sampled_hours = np.random.choice(hours, N_TRANSACTIONS, p=hour_weights)

transaction_ts = (
    pd.to_datetime(sampled_days)
    + pd.to_timedelta(sampled_hours, unit="h")
    + pd.to_timedelta(np.random.randint(0,60,N_TRANSACTIONS), unit="m")
    + pd.to_timedelta(np.random.randint(0,60,N_TRANSACTIONS), unit="s")
)

store_probs = np.random.dirichlet(np.ones(len(stores)))
store_id = np.random.choice(stores["store_id"], N_TRANSACTIONS, p=store_probs)

customer_id = np.random.choice(customers["customer_id"], N_TRANSACTIONS)
tier = customers.set_index("customer_id").loc[customer_id, "loyalty_tier"].to_numpy()

channels = np.array(["In-Store","Mobile Order","Drive-Thru","Delivery"], dtype=object)
promo_types = np.array(["None","BOGO","% Off","$ Off","Happy Hour","Loyalty Reward"], dtype=object)
payments = np.array(["Credit","Debit","Cash","Gift Card","Mobile Pay"], dtype=object)

# Tier-based channel/promo (vectorized-ish via masks)
channel = np.empty(N_TRANSACTIONS, dtype=object)
promo   = np.empty(N_TRANSACTIONS, dtype=object)

mask_gp = np.isin(tier, ["Gold","Platinum"])
mask_g  = tier == "Green"
mask_n  = ~ (mask_gp | mask_g)

channel[mask_gp] = np.random.choice(channels, mask_gp.sum(), p=[0.30,0.45,0.18,0.07])
promo[mask_gp]   = np.random.choice(promo_types, mask_gp.sum(), p=[0.62,0.07,0.08,0.05,0.07,0.11])

channel[mask_g]  = np.random.choice(channels, mask_g.sum(),  p=[0.42,0.30,0.22,0.06])
promo[mask_g]    = np.random.choice(promo_types, mask_g.sum(),  p=[0.74,0.06,0.07,0.05,0.04,0.04])

channel[mask_n]  = np.random.choice(channels, mask_n.sum(),  p=[0.62,0.12,0.20,0.06])
promo[mask_n]    = np.random.choice(promo_types, mask_n.sum(),  p=[0.90,0.03,0.03,0.03,0.01,0.00])

payment_method = np.random.choice(payments, N_TRANSACTIONS, p=[0.36,0.22,0.10,0.10,0.22])

emp_by_store = employees.groupby("store_id")["employee_id"].apply(list).to_dict()
employee_id = np.array([np.random.choice(emp_by_store[s]) for s in store_id], dtype=object)

order_wait_sec = np.clip(np.random.normal(240,120,N_TRANSACTIONS), 60, 900).astype(int)
is_refund = np.random.choice([0,1], N_TRANSACTIONS, p=[0.995,0.005])
refund_reason = np.where(is_refund==1, np.random.choice(["Wrong Item","Quality Issue","Late Delivery","Payment Error"], N_TRANSACTIONS), None)

transactions = pd.DataFrame({
    "transaction_id": [f"T{str(i).zfill(8)}" for i in range(1, N_TRANSACTIONS+1)],
    "transaction_ts": transaction_ts,
    "store_id": store_id,
    "customer_id": customer_id,
    "channel": channel,
    "payment_method": payment_method,
    "promo_type": promo,
    "order_wait_sec": order_wait_sec,
    "is_refund": is_refund,
    "refund_reason": refund_reason,
    "employee_id": employee_id
})

# ---------- FACT: LINE ITEMS ----------
item_counts = np.random.choice([1,2,3,4,5], N_TRANSACTIONS, p=[0.36,0.32,0.18,0.10,0.04])
rows = int(item_counts.sum())

tx_ids = np.repeat(transactions["transaction_id"].to_numpy(), item_counts)

prod_ids = products["product_id"].to_numpy()
cat_map  = products.set_index("product_id")["category"].to_dict()
price_map= products.set_index("product_id")["default_unit_price"].to_dict()
cogs_map = products.set_index("product_id")["unit_cogs"].to_dict()

cat_weights = {"Brewed Coffee":0.14,"Espresso":0.20,"Cold Brew":0.10,"Tea":0.10,"Frappé":0.06,"Bakery":0.18,"Sandwich":0.10,"Snack":0.08,"Merch":0.04}
prod_probs = np.array([cat_weights[cat_map[p]] for p in prod_ids])
prod_probs = prod_probs / prod_probs.sum()
product_id = np.random.choice(prod_ids, rows, p=prod_probs)

category = np.array([cat_map[p] for p in product_id], dtype=object)
is_drink = np.isin(category, ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])

size_opts = np.array(["Short","Tall","Grande","Venti"], dtype=object)
milk_opts = np.array(["None","2%","Whole","Oat","Almond","Soy","Nonfat"], dtype=object)
temp_opts = np.array(["Hot","Iced"], dtype=object)

size = np.where(is_drink, np.random.choice(size_opts, rows, p=[0.08,0.22,0.38,0.32]), None)
milk = np.where(is_drink, np.random.choice(milk_opts, rows, p=[0.32,0.26,0.10,0.14,0.08,0.06,0.04]), None)
temp = np.where(is_drink, np.random.choice(temp_opts, rows, p=[0.58,0.42]), None)

addon_shots = np.where(category=="Espresso", np.random.choice([0,1,2], rows, p=[0.60,0.30,0.10]), 0)
addon_syrup = np.where(is_drink, np.random.choice([0,1,2,3], rows, p=[0.55,0.28,0.12,0.05]), 0)

qty = np.ones(rows, dtype=int)
packable = np.isin(category, ["Snack","Merch","Bakery"])
qty[packable] = np.random.choice([1,2,3], packable.sum(), p=[0.85,0.12,0.03])

base_price = np.array([price_map[p] for p in product_id])
base_cogs  = np.array([cogs_map[p] for p in product_id])

size_mult = pd.Series(size).map({"Short":0.92,"Tall":1.00,"Grande":1.12,"Venti":1.25}).fillna(1.0).to_numpy()
addon_price = addon_shots*0.95 + addon_syrup*0.65
unit_price = np.round(base_price*size_mult + addon_price, 2)

items = pd.DataFrame({
    "transaction_id": tx_ids,
    "line_nbr": 0,
    "product_id": product_id,
    "category": category,
    "size": size,
    "milk": milk,
    "temp": temp,
    "addon_shots": addon_shots,
    "addon_syrup_pumps": addon_syrup,
    "qty": qty,
    "unit_price": unit_price,
    "unit_cogs": np.round(base_cogs,2),
    "line_discount": 0.0
})
items["line_nbr"] = items.groupby("transaction_id").cumcount() + 1

# Apply promo discounts
promo_map = transactions.set_index("transaction_id")["promo_type"].to_dict()
promo_for_item = items["transaction_id"].map(promo_map).to_numpy()

disc = np.zeros(rows)
mask = promo_for_item == "% Off"
disc[mask] = np.round(items.loc[mask,"unit_price"].to_numpy() * np.random.uniform(0.10,0.25, mask.sum()), 2)

mask = promo_for_item == "$ Off"
disc[mask] = np.round(np.random.uniform(0.50,2.50, mask.sum()), 2)

mask = (promo_for_item == "Happy Hour") & np.isin(items["category"].to_numpy(), ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])
disc[mask] = np.round(items.loc[mask,"unit_price"].to_numpy() * 0.20, 2)

mask_lr = promo_for_item == "Loyalty Reward"
idx_lr_drink = items.index[mask_lr & np.isin(items["category"].to_numpy(), ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])].to_numpy()
if len(idx_lr_drink) > 0:
    free_idx = np.random.choice(idx_lr_drink, size=max(1, int(0.12*len(idx_lr_drink))), replace=False)
    disc[free_idx] = items.loc[free_idx, "unit_price"].to_numpy()

items["line_discount"] = disc

# Compute transaction totals
line_sub = np.round(items["qty"]*items["unit_price"], 2)
line_disc= np.round(items["qty"]*items["line_discount"], 2)
line_net = np.round(line_sub - line_disc, 2)
line_cogs= np.round(items["qty"]*items["unit_cogs"], 2)

agg = pd.DataFrame({
    "transaction_id": items["transaction_id"],
    "item_lines": items["line_nbr"],
    "units": items["qty"],
    "subtotal": line_sub,
    "discount": line_disc,
    "net_sales": line_net,
    "cogs": line_cogs
}).groupby("transaction_id", as_index=False).agg({
    "item_lines":"max",
    "units":"sum",
    "subtotal":"sum",
    "discount":"sum",
    "net_sales":"sum",
    "cogs":"sum"
})

transactions = transactions.merge(agg, on="transaction_id", how="left")

TAX_RATE = 0.102
tips = np.where(np.isin(transactions["channel"], ["In-Store","Drive-Thru"]), np.round(np.random.exponential(0.85, N_TRANSACTIONS),2), 0.0)
tips = np.clip(tips, 0, 8.00)

transactions["tax"] = np.round(transactions["net_sales"] * TAX_RATE, 2)
transactions["tip"] = tips
transactions["total_amount"] = np.round(transactions["net_sales"] + transactions["tax"] + transactions["tip"], 2)
transactions["gross_margin"] = np.round(transactions["net_sales"] - transactions["cogs"], 2)
transactions["gm_pct"] = np.round(np.where(transactions["net_sales"]>0, transactions["gross_margin"]/transactions["net_sales"], 0), 4)

base_service = np.select(
    [transactions["channel"]=="Mobile Order", transactions["channel"]=="Delivery", transactions["channel"]=="Drive-Thru"],
    [180, 260, 210],
    default=240
)
transactions["service_time_sec"] = np.clip((base_service + transactions["item_lines"]*35 + np.random.normal(0,35,N_TRANSACTIONS)).astype(int), 60, 1200)

# Refund reversals
refund_mask = transactions["is_refund"] == 1
for col in ["subtotal","discount","net_sales","tax","tip","total_amount","gross_margin"]:
    transactions.loc[refund_mask, col] *= -1

# ---------- EXPORT ----------
stores.to_csv(OUT_DIR/"coffee_stores.csv", index=False)
products.to_csv(OUT_DIR/"coffee_products.csv", index=False)
customers.to_csv(OUT_DIR/"coffee_customers.csv", index=False)
employees.to_csv(OUT_DIR/"coffee_employees.csv", index=False)
transactions.to_csv(OUT_DIR/"coffee_transactions.csv", index=False)
items.to_csv(OUT_DIR/"coffee_transaction_items.csv", index=False)

# One Excel workbook (pivot-ready) — guarded in case the Excel writer fails
try:
    with pd.ExcelWriter(OUT_DIR/"coffee_analytics_dataset.xlsx", engine="openpyxl") as writer:
        stores.to_excel(writer, "dim_stores", index=False)
        products.to_excel(writer, "dim_products", index=False)
        customers.to_excel(writer, "dim_customers", index=False)
        employees.to_excel(writer, "dim_employees", index=False)
        transactions.to_excel(writer, "fact_transactions", index=False)
        items.to_excel(writer, "fact_items", index=False)
except Exception as e:
    print("⚠️ Excel export failed:", e)

print("✅ Done. Files in:", OUT_DIR.resolve())
print("Transactions:", len(transactions), "Items:", len(items))

import numpy as np
import pandas as pd
from pathlib import Path

# ---------- CONFIG ----------
N_TRANSACTIONS = 120_000        # 100k+
SEED = 42
OUT_DIR = Path("coffee_dataset_out")

START = pd.Timestamp("2025-01-01")
END   = pd.Timestamp("2025-12-31 23:59:59")

# ---------- SETUP ----------
np.random.seed(SEED)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- DIM: STORES ----------
n_stores = 35
cities = ["Seattle","Bellevue","Redmond","Tacoma","Everett","Kirkland","Renton","Bothell","Issaquah","Olympia"]
store_types = ["Urban","Suburban","Drive-Thru","Campus","Airport","Grocery Kiosk"]
regions = ["PNW-North","PNW-Central","PNW-South"]

stores = pd.DataFrame({
    "store_id": [f"S{str(i).zfill(3)}" for i in range(1, n_stores+1)],
    "store_name": [f"BeanBrew #{i:03d}" for i in range(1, n_stores+1)],
    "city": np.random.choice(cities, n_stores),
    "region": np.random.choice(regions, n_stores, p=[0.35,0.40,0.25]),
    "store_type": np.random.choice(store_types, n_stores, p=[0.35,0.30,0.20,0.10,0.03,0.02]),
    "open_date": pd.to_datetime(np.random.choice(pd.date_range("2014-01-01","2024-12-31"), n_stores)).date
})

# ---------- DIM: PRODUCTS ----------
categories = ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé","Bakery","Sandwich","Snack","Merch"]
base_price_map = {
    "Brewed Coffee": (2.25, 4.75),
    "Espresso":      (3.25, 6.75),
    "Cold Brew":     (3.75, 6.95),
    "Tea":           (2.95, 6.25),
    "Frappé":        (4.25, 7.45),
    "Bakery":        (2.25, 5.95),
    "Sandwich":      (4.95, 9.95),
    "Snack":         (1.25, 4.95),
    "Merch":         (6.95, 29.95)
}

n_products = 120
product_category = np.random.choice(categories, n_products, p=[0.14,0.18,0.10,0.10,0.06,0.16,0.10,0.10,0.06])

def make_name(cat):
    if cat in ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"]:
        flavor = np.random.choice(["House","Mocha","Vanilla","Caramel","Hazelnut","Matcha","Chai","Toffee","Cinnamon","Pumpkin"])
        style  = np.random.choice(["Latte","Americano","Cappuccino","Macchiato","Mocha","Brew","Nitro","Refresher","Tea","Frap"])
        return f"{flavor} {style}"
    if cat == "Bakery":
        return np.random.choice(["Croissant","Blueberry Muffin","Banana Bread","Cinnamon Roll","Scone","Cookie","Brownie","Cake Pop"])
    if cat == "Sandwich":
        return np.random.choice(["Turkey & Swiss","Bacon Gouda","Egg & Cheddar","Ham & Cheese","Veggie Wrap","Chicken Panini"])
    if cat == "Snack":
        return np.random.choice(["Chips","Protein Bar","Trail Mix","Fruit Cup","Yogurt","Jerky"])
    return np.random.choice(["Tumbler","Mug","Beans 12oz","Beans 2lb","Gift Card","Sticker Pack","French Press"])

names = [make_name(c) for c in product_category]
prices, cogs = [], []
for cat in product_category:
    lo, hi = base_price_map[cat]
    p = np.round(np.random.uniform(lo, hi), 2)
    prices.append(p)
    c = p * np.random.uniform(0.22, 0.55) if cat != "Merch" else p * np.random.uniform(0.45, 0.70)
    cogs.append(np.round(c, 2))

products = pd.DataFrame({
    "product_id": [f"P{str(i).zfill(4)}" for i in range(1, n_products+1)],
    "product_name": names,
    "category": product_category,
    "default_unit_price": prices,
    "unit_cogs": cogs,
    "is_seasonal": np.random.choice([0,1], n_products, p=[0.85,0.15])
}).drop_duplicates(subset=["product_name","category"]).reset_index(drop=True)
products["product_id"] = [f"P{str(i).zfill(4)}" for i in range(1, len(products)+1)]

# ---------- DIM: CUSTOMERS ----------
n_customers = 42_000
first_names = ["Alex","Sam","Jordan","Taylor","Morgan","Casey","Riley","Jamie","Avery","Cameron","Parker","Quinn","Skyler","Reese","Rowan"]
last_names  = ["Lee","Nguyen","Patel","Garcia","Smith","Johnson","Brown","Davis","Wilson","Martinez","Anderson","Thomas","Jackson","White","Harris"]
domains     = ["gmail.com","yahoo.com","outlook.com","icloud.com","hotmail.com"]

def rand_phone(n):
    a = np.random.randint(200,999,n)
    b = np.random.randint(200,999,n)
    c = np.random.randint(1000,9999,n)
    return [f"{a[i]}-{b[i]}-{c[i]}" for i in range(n)]

customers = pd.DataFrame({
    "customer_id": [f"C{str(i).zfill(6)}" for i in range(1, n_customers+1)],
    "first_name": np.random.choice(first_names, n_customers),
    "last_name":  np.random.choice(last_names, n_customers),
    "phone": rand_phone(n_customers),
    "loyalty_tier": np.random.choice(["None","Green","Gold","Platinum"], n_customers, p=[0.35,0.35,0.22,0.08]),
    "signup_date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01","2025-12-31"), n_customers)).date,
    "marketing_opt_in": np.random.choice([0,1], n_customers, p=[0.45,0.55]),
})
customers["email"] = (
    customers["first_name"].str.lower() + "." +
    customers["last_name"].str.lower() +
    np.random.randint(1,9999,n_customers).astype(str) + "@" +
    np.random.choice(domains, n_customers)
)

# ---------- DIM: EMPLOYEES ----------
n_employees = 420
employees = pd.DataFrame({
    "employee_id": [f"E{str(i).zfill(5)}" for i in range(1, n_employees+1)],
    "store_id": np.random.choice(stores["store_id"], n_employees),
    "role": np.random.choice(["Barista","Shift Supervisor","Cashier"], n_employees, p=[0.72,0.18,0.10]),
    "hire_date": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01","2025-12-31"), n_employees)).date,
    "hourly_rate": np.round(np.random.uniform(17.5, 27.5, n_employees), 2)
})

# ---------- FACT: TRANSACTIONS (VECTOR WEIGHTED TIME) ----------
all_days = pd.date_range(START.date(), END.date(), freq="D")
dow_weights = np.array([1.02,1.04,1.05,1.06,1.10,0.92,0.88])
dow_weights = dow_weights / dow_weights.sum()
day_probs = dow_weights[all_days.dayofweek.values]
day_probs = day_probs / day_probs.sum()
sampled_days = np.random.choice(all_days, N_TRANSACTIONS, p=day_probs)

hours = np.arange(5, 22)
hour_weights = np.array([0.02,0.03,0.05,0.08,0.10,0.11,0.10,0.08,0.06,0.05,0.04,0.04,0.05,0.06,0.05,0.04,0.03])
hour_weights = hour_weights / hour_weights.sum()
sampled_hours = np.random.choice(hours, N_TRANSACTIONS, p=hour_weights)

transaction_ts = (
    pd.to_datetime(sampled_days)
    + pd.to_timedelta(sampled_hours, unit="h")
    + pd.to_timedelta(np.random.randint(0,60,N_TRANSACTIONS), unit="m")
    + pd.to_timedelta(np.random.randint(0,60,N_TRANSACTIONS), unit="s")
)

store_probs = np.random.dirichlet(np.ones(len(stores)))
store_id = np.random.choice(stores["store_id"], N_TRANSACTIONS, p=store_probs)

customer_id = np.random.choice(customers["customer_id"], N_TRANSACTIONS)
tier = customers.set_index("customer_id").loc[customer_id, "loyalty_tier"].to_numpy()

channels = np.array(["In-Store","Mobile Order","Drive-Thru","Delivery"], dtype=object)
promo_types = np.array(["None","BOGO","% Off","$ Off","Happy Hour","Loyalty Reward"], dtype=object)
payments = np.array(["Credit","Debit","Cash","Gift Card","Mobile Pay"], dtype=object)

# Tier-based channel/promo (vectorized-ish via masks)
channel = np.empty(N_TRANSACTIONS, dtype=object)
promo   = np.empty(N_TRANSACTIONS, dtype=object)

mask_gp = np.isin(tier, ["Gold","Platinum"])
mask_g  = tier == "Green"
mask_n  = ~ (mask_gp | mask_g)

channel[mask_gp] = np.random.choice(channels, mask_gp.sum(), p=[0.30,0.45,0.18,0.07])
promo[mask_gp]   = np.random.choice(promo_types, mask_gp.sum(), p=[0.62,0.07,0.08,0.05,0.07,0.11])

channel[mask_g]  = np.random.choice(channels, mask_g.sum(),  p=[0.42,0.30,0.22,0.06])
promo[mask_g]    = np.random.choice(promo_types, mask_g.sum(),  p=[0.74,0.06,0.07,0.05,0.04,0.04])

channel[mask_n]  = np.random.choice(channels, mask_n.sum(),  p=[0.62,0.12,0.20,0.06])
promo[mask_n]    = np.random.choice(promo_types, mask_n.sum(),  p=[0.90,0.03,0.03,0.03,0.01,0.00])

payment_method = np.random.choice(payments, N_TRANSACTIONS, p=[0.36,0.22,0.10,0.10,0.22])

emp_by_store = employees.groupby("store_id")["employee_id"].apply(list).to_dict()
employee_id = np.array([np.random.choice(emp_by_store[s]) for s in store_id], dtype=object)

order_wait_sec = np.clip(np.random.normal(240,120,N_TRANSACTIONS), 60, 900).astype(int)
is_refund = np.random.choice([0,1], N_TRANSACTIONS, p=[0.995,0.005])
refund_reason = np.where(is_refund==1, np.random.choice(["Wrong Item","Quality Issue","Late Delivery","Payment Error"], N_TRANSACTIONS), None)

transactions = pd.DataFrame({
    "transaction_id": [f"T{str(i).zfill(8)}" for i in range(1, N_TRANSACTIONS+1)],
    "transaction_ts": transaction_ts,
    "store_id": store_id,
    "customer_id": customer_id,
    "channel": channel,
    "payment_method": payment_method,
    "promo_type": promo,
    "order_wait_sec": order_wait_sec,
    "is_refund": is_refund,
    "refund_reason": refund_reason,
    "employee_id": employee_id
})

# ---------- FACT: LINE ITEMS ----------
item_counts = np.random.choice([1,2,3,4,5], N_TRANSACTIONS, p=[0.36,0.32,0.18,0.10,0.04])
rows = int(item_counts.sum())

tx_ids = np.repeat(transactions["transaction_id"].to_numpy(), item_counts)

prod_ids = products["product_id"].to_numpy()
cat_map  = products.set_index("product_id")["category"].to_dict()
price_map= products.set_index("product_id")["default_unit_price"].to_dict()
cogs_map = products.set_index("product_id")["unit_cogs"].to_dict()

cat_weights = {"Brewed Coffee":0.14,"Espresso":0.20,"Cold Brew":0.10,"Tea":0.10,"Frappé":0.06,"Bakery":0.18,"Sandwich":0.10,"Snack":0.08,"Merch":0.04}
prod_probs = np.array([cat_weights[cat_map[p]] for p in prod_ids])
prod_probs = prod_probs / prod_probs.sum()
product_id = np.random.choice(prod_ids, rows, p=prod_probs)

category = np.array([cat_map[p] for p in product_id], dtype=object)
is_drink = np.isin(category, ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])

size_opts = np.array(["Short","Tall","Grande","Venti"], dtype=object)
milk_opts = np.array(["None","2%","Whole","Oat","Almond","Soy","Nonfat"], dtype=object)
temp_opts = np.array(["Hot","Iced"], dtype=object)

size = np.where(is_drink, np.random.choice(size_opts, rows, p=[0.08,0.22,0.38,0.32]), None)
milk = np.where(is_drink, np.random.choice(milk_opts, rows, p=[0.32,0.26,0.10,0.14,0.08,0.06,0.04]), None)
temp = np.where(is_drink, np.random.choice(temp_opts, rows, p=[0.58,0.42]), None)

addon_shots = np.where(category=="Espresso", np.random.choice([0,1,2], rows, p=[0.60,0.30,0.10]), 0)
addon_syrup = np.where(is_drink, np.random.choice([0,1,2,3], rows, p=[0.55,0.28,0.12,0.05]), 0)

qty = np.ones(rows, dtype=int)
packable = np.isin(category, ["Snack","Merch","Bakery"])
qty[packable] = np.random.choice([1,2,3], packable.sum(), p=[0.85,0.12,0.03])

base_price = np.array([price_map[p] for p in product_id])
base_cogs  = np.array([cogs_map[p] for p in product_id])

size_mult = pd.Series(size).map({"Short":0.92,"Tall":1.00,"Grande":1.12,"Venti":1.25}).fillna(1.0).to_numpy()
addon_price = addon_shots*0.95 + addon_syrup*0.65
unit_price = np.round(base_price*size_mult + addon_price, 2)

items = pd.DataFrame({
    "transaction_id": tx_ids,
    "line_nbr": 0,
    "product_id": product_id,
    "category": category,
    "size": size,
    "milk": milk,
    "temp": temp,
    "addon_shots": addon_shots,
    "addon_syrup_pumps": addon_syrup,
    "qty": qty,
    "unit_price": unit_price,
    "unit_cogs": np.round(base_cogs,2),
    "line_discount": 0.0
})
items["line_nbr"] = items.groupby("transaction_id").cumcount() + 1

# Apply promo discounts
promo_map = transactions.set_index("transaction_id")["promo_type"].to_dict()
promo_for_item = items["transaction_id"].map(promo_map).to_numpy()

disc = np.zeros(rows)
mask = promo_for_item == "% Off"
disc[mask] = np.round(items.loc[mask,"unit_price"].to_numpy() * np.random.uniform(0.10,0.25, mask.sum()), 2)

mask = promo_for_item == "$ Off"
disc[mask] = np.round(np.random.uniform(0.50,2.50, mask.sum()), 2)

mask = (promo_for_item == "Happy Hour") & np.isin(items["category"].to_numpy(), ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])
disc[mask] = np.round(items.loc[mask,"unit_price"].to_numpy() * 0.20, 2)

mask_lr = promo_for_item == "Loyalty Reward"
idx_lr_drink = items.index[mask_lr & np.isin(items["category"].to_numpy(), ["Brewed Coffee","Espresso","Cold Brew","Tea","Frappé"])].to_numpy()
if len(idx_lr_drink) > 0:
    free_idx = np.random.choice(idx_lr_drink, size=max(1, int(0.12*len(idx_lr_drink))), replace=False)
    disc[free_idx] = items.loc[free_idx, "unit_price"].to_numpy()

items["line_discount"] = disc

# Compute transaction totals
line_sub = np.round(items["qty"]*items["unit_price"], 2)
line_disc= np.round(items["qty"]*items["line_discount"], 2)
line_net = np.round(line_sub - line_disc, 2)
line_cogs= np.round(items["qty"]*items["unit_cogs"], 2)

agg = pd.DataFrame({
    "transaction_id": items["transaction_id"],
    "item_lines": items["line_nbr"],
    "units": items["qty"],
    "subtotal": line_sub,
    "discount": line_disc,
    "net_sales": line_net,
    "cogs": line_cogs
}).groupby("transaction_id", as_index=False).agg({
    "item_lines":"max",
    "units":"sum",
    "subtotal":"sum",
    "discount":"sum",
    "net_sales":"sum",
    "cogs":"sum"
})

transactions = transactions.merge(agg, on="transaction_id", how="left")

TAX_RATE = 0.102
tips = np.where(np.isin(transactions["channel"], ["In-Store","Drive-Thru"]), np.round(np.random.exponential(0.85, N_TRANSACTIONS),2), 0.0)
tips = np.clip(tips, 0, 8.00)

transactions["tax"] = np.round(transactions["net_sales"] * TAX_RATE, 2)
transactions["tip"] = tips
transactions["total_amount"] = np.round(transactions["net_sales"] + transactions["tax"] + transactions["tip"], 2)
transactions["gross_margin"] = np.round(transactions["net_sales"] - transactions["cogs"], 2)
transactions["gm_pct"] = np.round(np.where(transactions["net_sales"]>0, transactions["gross_margin"]/transactions["net_sales"], 0), 4)

base_service = np.select(
    [transactions["channel"]=="Mobile Order", transactions["channel"]=="Delivery", transactions["channel"]=="Drive-Thru"],
    [180, 260, 210],
    default=240
)
transactions["service_time_sec"] = np.clip((base_service + transactions["item_lines"]*35 + np.random.normal(0,35,N_TRANSACTIONS)).astype(int), 60, 1200)

# Refund reversals
refund_mask = transactions["is_refund"] == 1
for col in ["subtotal","discount","net_sales","tax","tip","total_amount","gross_margin"]:
    transactions.loc[refund_mask, col] *= -1

# ---------- EXPORT ----------
stores.to_csv(OUT_DIR/"coffee_stores.csv", index=False)
products.to_csv(OUT_DIR/"coffee_products.csv", index=False)
customers.to_csv(OUT_DIR/"coffee_customers.csv", index=False)
employees.to_csv(OUT_DIR/"coffee_employees.csv", index=False)
transactions.to_csv(OUT_DIR/"coffee_transactions.csv", index=False)
items.to_csv(OUT_DIR/"coffee_transaction_items.csv", index=False)

# One Excel workbook (pivot-ready)
with pd.ExcelWriter(OUT_DIR/"coffee_analytics_dataset.xlsx", engine="openpyxl") as writer:
    stores.to_excel(writer, "dim_stores", index=False)
    products.to_excel(writer, "dim_products", index=False)
    customers.to_excel(writer, "dim_customers", index=False)
    employees.to_excel(writer, "dim_employees", index=False)
    transactions.to_excel(writer, "fact_transactions", index=False)
    items.to_excel(writer, "fact_items", index=False)

print("✅ Done. Files in:", OUT_DIR.resolve())
print("Transactions:", len(transactions), "Items:", len(items))



