"""
Data ingestion, synthetic generation, and feature engineering module.
Produces a realistic multi-year transactional dataset for executive retail analytics.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from src.config import RAW_DATA_PATH, PROCESSED_DATA_PATH


def generate_synthetic_sales_data(num_records: int = 3200, seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic multi-year transactional retail dataset (2023 - 2026).
    Embeds realistic business dynamics:
    - Q4 holiday sales surges (Nov-Dec seasonality)
    - Margin erosion from aggressive discounting (>20%)
    - Regional variations and customer segment distributions
    - Unprofitable sub-categories (e.g. Tables, Machines) due to high freight & discounting
    """
    np.random.seed(seed)
    
    # 1. Temporal distribution (2023-01-01 to 2026-06-30)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days
    
    # Generate dates with Q4 seasonality weighting
    raw_days = np.random.randint(0, total_days, size=num_records)
    dates = [start_date + timedelta(days=int(d)) for d in raw_days]
    
    # Boost Q4 transactions (Nov & Dec) by shifting a portion of dates
    adjusted_dates = []
    for d in dates:
        if np.random.rand() < 0.25:
            # Shift into Nov-Dec of that year
            year = d.year
            month = np.random.choice([11, 12])
            day = np.random.randint(1, 29)
            adjusted_dates.append(datetime(year, month, day))
        else:
            adjusted_dates.append(d)
    adjusted_dates.sort()

    # 2. Customers (~450 unique customers)
    num_customers = 450
    customer_ids = [f"CUST-{i:04d}" for i in range(1, num_customers + 1)]
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                   "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                   "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                  "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"]
    customer_names = {cid: f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for cid in customer_ids}
    
    assigned_cust_ids = np.random.choice(customer_ids, size=num_records, p=np.random.dirichlet(np.ones(num_customers) * 0.7))
    assigned_cust_names = [customer_names[cid] for cid in assigned_cust_ids]

    # 3. Customer Segments
    segments = ["Consumer", "Corporate", "Home Office"]
    segment_weights = [0.52, 0.30, 0.18]
    cust_segment_map = {cid: np.random.choice(segments, p=segment_weights) for cid in customer_ids}
    assigned_segments = [cust_segment_map[cid] for cid in assigned_cust_ids]

    # 4. Geographies & Regions
    regions = {
        "West": ["California", "Washington", "Oregon", "Nevada", "Arizona", "Colorado"],
        "East": ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Ohio"],
        "Central": ["Illinois", "Texas", "Michigan", "Indiana", "Wisconsin"],
        "South": ["Florida", "Georgia", "North Carolina", "Virginia", "Tennessee"]
    }
    region_names = list(regions.keys())
    region_weights = [0.32, 0.28, 0.22, 0.18]
    assigned_regions = np.random.choice(region_names, size=num_records, p=region_weights)
    assigned_states = [np.random.choice(regions[r]) for r in assigned_regions]

    # 5. Product Hierarchy
    products = {
        "Technology": {
            "Phones": (150, 950, 0.25),
            "Accessories": (30, 180, 0.35),
            "Copiers": (400, 2400, 0.40),
            "Machines": (250, 1500, 0.05)  # Problematic margin
        },
        "Furniture": {
            "Chairs": (100, 450, 0.15),
            "Bookcases": (80, 350, 0.02),   # High freight loss
            "Tables": (150, 650, -0.08),    # Chronic loss leader
            "Furnishings": (20, 120, 0.20)
        },
        "Office Supplies": {
            "Storage": (40, 220, 0.22),
            "Binders": (5, 65, 0.38),
            "Paper": (10, 80, 0.42),
            "Appliances": (60, 320, 0.20),
            "Art": (8, 50, 0.30),
            "Envelopes": (6, 35, 0.40),
            "Labels": (5, 30, 0.45),
            "Fasteners": (4, 25, 0.35),
            "Supplies": (12, 90, 0.10)
        }
    }
    
    categories = list(products.keys())
    cat_weights = [0.35, 0.30, 0.35]
    assigned_cats = np.random.choice(categories, size=num_records, p=cat_weights)
    
    assigned_subcats = []
    base_costs = []
    base_margins = []
    
    for cat in assigned_cats:
        subcat_dict = products[cat]
        subcat_names = list(subcat_dict.keys())
        chosen_subcat = np.random.choice(subcat_names)
        low_cost, high_cost, target_margin = subcat_dict[chosen_subcat]
        assigned_subcats.append(chosen_subcat)
        unit_cost = np.random.uniform(low_cost, high_cost)
        base_costs.append(unit_cost)
        base_margins.append(target_margin)

    # 6. Quantities and Discounts
    quantities = np.random.choice(range(1, 11), size=num_records, p=[0.25, 0.22, 0.18, 0.12, 0.08, 0.05, 0.04, 0.03, 0.02, 0.01])
    
    # Discounts: realistic discrete promotional discounts (0%, 10%, 15%, 20%, 30%, 50%, 70%)
    discount_choices = [0.0, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.70]
    discount_probs = [0.45, 0.18, 0.12, 0.10, 0.07, 0.04, 0.03, 0.01]
    discounts = np.random.choice(discount_choices, size=num_records, p=discount_probs)

    # 7. Financial Calculations (Sales, Profit, Shipping Cost)
    sales = []
    profits = []
    shipping_costs = []
    ship_modes = []
    ship_dates = []
    ship_options = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_weights = [0.60, 0.20, 0.15, 0.05]
    
    for i in range(num_records):
        qty = quantities[i]
        cost = base_costs[i]
        disc = discounts[i]
        tgt_margin = base_margins[i]
        
        # Base unit selling price before discount
        unit_list_price = cost / (1 - max(tgt_margin, 0.05))
        total_list_sales = unit_list_price * qty
        final_sales = total_list_sales * (1 - disc)
        
        # Shipping Mode & Duration
        smode = np.random.choice(ship_options, p=ship_weights)
        ship_modes.append(smode)
        
        if smode == "Same Day":
            ship_days = 0
            ship_mult = 1.6
        elif smode == "First Class":
            ship_days = np.random.choice([1, 2])
            ship_mult = 1.3
        elif smode == "Second Class":
            ship_days = np.random.choice([3, 4])
            ship_mult = 1.0
        else:
            ship_days = np.random.choice([5, 6, 7])
            ship_mult = 0.7
            
        ship_dates.append(adjusted_dates[i] + timedelta(days=int(ship_days)))
        
        # Shipping Cost
        base_ship = (final_sales * 0.04 + qty * 3.5) * ship_mult
        shipping_costs.append(round(base_ship, 2))
        
        # Total cost = COGS + Shipping subsidy + handling
        total_cogs = cost * qty
        # Profit = Sales - COGS - (portion of ship cost if free shipping promo)
        freight_burden = base_ship * (0.5 if disc > 0.15 else 0.2)
        profit_val = final_sales - total_cogs - freight_burden
        
        # Introduce natural variance / noise
        noise = np.random.normal(0, max(final_sales * 0.03, 5))
        profit_val += noise
        
        sales.append(round(final_sales, 2))
        profits.append(round(profit_val, 2))

    # 8. Order Priorities & Order IDs
    order_priorities = np.random.choice(["Medium", "High", "Critical", "Low"], size=num_records, p=[0.55, 0.25, 0.12, 0.08])
    order_ids = [f"ORD-{d.year}-{10000 + i}" for i, d in enumerate(adjusted_dates)]

    # Assemble raw DataFrame
    df = pd.DataFrame({
        "Order_ID": order_ids,
        "Order_Date": [d.strftime("%Y-%m-%d") for d in adjusted_dates],
        "Ship_Date": [d.strftime("%Y-%m-%d") for d in ship_dates],
        "Ship_Mode": ship_modes,
        "Customer_ID": assigned_cust_ids,
        "Customer_Name": assigned_cust_names,
        "Customer_Segment": assigned_segments,
        "Country": "United States",
        "Region": assigned_regions,
        "State": assigned_states,
        "Category": assigned_cats,
        "Sub_Category": assigned_subcats,
        "Sales": sales,
        "Quantity": quantities,
        "Discount": discounts,
        "Profit": profits,
        "Shipping_Cost": shipping_costs,
        "Order_Priority": order_priorities
    })
    
    # Persist raw dataset
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f" Generated raw dataset with {len(df):,} records at: {RAW_DATA_PATH}")
    return df


def clean_and_engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataset and computes executive analytical features:
    - Profit_Margin_Pct: (Profit / Sales) * 100
    - Discount_Tier: Categorical grouping for elasticity analysis
    - Shipping_Duration_Days: Lead time calculation
    - Temporal features: Year, Month, Year_Month, Quarter
    - Unit economics: Sales_Per_Unit, Profit_Per_Unit
    """
    df = df.copy()
    
    # 1. Parse dates
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    
    # 2. Temporal Features
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Year_Quarter"] = df["Year"].astype(str) + " " + df["Quarter"]
    
    # 3. Operational Features
    df["Shipping_Duration_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days
    
    # 4. Financial & Margin Features
    # Avoid zero-division in edge cases
    df["Profit_Margin_Pct"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, 0.0)
    df["Profit_Margin_Pct"] = df["Profit_Margin_Pct"].round(2)
    
    df["Sales_Per_Unit"] = (df["Sales"] / df["Quantity"]).round(2)
    df["Profit_Per_Unit"] = (df["Profit"] / df["Quantity"]).round(2)
    
    # 5. Discount Tiers for Segmentation
    bins = [-0.01, 0.00, 0.10, 0.20, 0.40, 1.00]
    labels = ["No Discount (0%)", "Low (1-10%)", "Moderate (11-20%)", "High (21-40%)", "Severe (>40%)"]
    df["Discount_Tier"] = pd.cut(df["Discount"], bins=bins, labels=labels)
    
    # 6. Profitability Status Flag
    df["Is_Profitable"] = df["Profit"] > 0
    df["Profit_Status"] = np.where(df["Profit"] > 0, "Profitable", "Loss-Making")

    # Persist processed dataset
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f" Cleaned & engineered dataset saved at: {PROCESSED_DATA_PATH}")
    return df


def load_data(force_regenerate: bool = False) -> pd.DataFrame:
    """
    Loads the cleaned analytical dataset. If not found or force_regenerate is True,
    generates and processes the dataset from scratch.
    """
    if force_regenerate or not PROCESSED_DATA_PATH.exists():
        raw_df = generate_synthetic_sales_data()
        return clean_and_engineer_features(raw_df)
    
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    return df


if __name__ == "__main__":
    df = load_data(force_regenerate=True)
    print(f"Successfully loaded {len(df):,} records.")
    print("Columns:", df.columns.tolist())
    print("\nHead preview:\n", df.head(3))
