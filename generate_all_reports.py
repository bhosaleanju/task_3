"""
Master Pipeline Script for Task 3: Data Visualization.
Executes the end-to-end workflow:
1. Generates & cleans multi-year retail transactions.
2. Computes executive KPIs and strategic metrics.
3. Renders and exports 5 high-resolution (300 DPI) publication figures.
4. Generates an executive summary markdown report.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data
from src.visualizer import generate_all_figures
from src.storytelling import generate_executive_narrative, compute_executive_kpis
from src.config import REPORTS_DIR


def main():
    print("=" * 70)
    print("TASK 3: DATA VISUALIZATION - EXECUTIVE PIPELINE EXECUTION")
    print("=" * 70)
    
    # 1. Load and process data
    print("\n[Step 1/4] Ingesting and engineering features...")
    df = load_data(force_regenerate=False)
    print(f" Loaded dataset: {len(df):,} records, {len(df.columns)} columns.")
    
    # 2. Compute Executive KPIs
    print("\n[Step 2/4] Computing executive metrics...")
    kpis = compute_executive_kpis(df)
    print(f" Total Revenue:       ${kpis['total_sales']:>14,.2f}")
    print(f" Net Operating Profit:${kpis['total_profit']:>14,.2f}")
    print(f" Operating Margin:    {kpis['profit_margin_pct']:>14.2f}%")
    print(f" Total Transactions:  {kpis['total_orders']:>14,}")
    print(f" Active Customers:    {kpis['unique_customers']:>14,}")
    print(f" Average Order Value: ${kpis['avg_order_value']:>14,.2f}")
    
    # 3. Render and export figures
    print("\n[Step 3/4] Generating 300-DPI publication figures...")
    generate_all_figures(df)
    
    # 4. Write Executive Summary Briefing
    print("[Step 4/4] Synthesizing Executive Decision Memo...")
    narrative = generate_executive_narrative(df)
    summary_path = REPORTS_DIR / "EXECUTIVE_SUMMARY.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(narrative)
    print(f" Saved executive memo to: {summary_path}")
    
    print("\n" + "=" * 70)
    print(" PIPELINE COMPLETED SUCCESSFULLY!")
    print("  - Figures saved in: reports/figures/")
    print("  - Executive Memo:   reports/EXECUTIVE_SUMMARY.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
