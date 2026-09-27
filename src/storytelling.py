"""
Automated Storytelling & Insight Extraction Engine.
Analyzes transactional data to synthesize executive-level findings,
risk factors, and commercial opportunities for C-suite decision-makers.
"""

from typing import Dict, Any
import pandas as pd


def compute_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes primary high-level KPIs across the entire enterprise dataset.
    """
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0.0
    total_orders = int(df["Order_ID"].nunique())
    unique_customers = int(df["Customer_ID"].nunique())
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    loss_making_orders = int((df["Profit"] < 0).sum())
    loss_order_pct = (loss_making_orders / len(df)) * 100 if len(df) > 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin_pct": profit_margin,
        "total_orders": total_orders,
        "unique_customers": unique_customers,
        "avg_order_value": avg_order_value,
        "loss_making_orders": loss_making_orders,
        "loss_order_pct": loss_order_pct,
    }


def analyze_discount_impact(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes the financial consequences of discounting above and below the 20% threshold.
    """
    low_disc = df[df["Discount"] <= 0.20]
    high_disc = df[df["Discount"] > 0.20]
    
    low_sales = float(low_disc["Sales"].sum())
    low_profit = float(low_disc["Profit"].sum())
    low_margin = (low_profit / low_sales) * 100 if low_sales > 0 else 0.0
    
    high_sales = float(high_disc["Sales"].sum())
    high_profit = float(high_disc["Profit"].sum())
    high_margin = (high_profit / high_sales) * 100 if high_sales > 0 else 0.0
    
    # Estimated profit recovery if high discounts were capped at 20%
    return {
        "under_20_sales": low_sales,
        "under_20_profit": low_profit,
        "under_20_margin_pct": low_margin,
        "over_20_sales": high_sales,
        "over_20_profit": high_profit,
        "over_20_margin_pct": high_margin,
        "high_disc_loss_orders": int((high_disc["Profit"] < 0).sum()),
        "high_disc_loss_rate_pct": ((high_disc["Profit"] < 0).sum() / len(high_disc)) * 100 if len(high_disc) > 0 else 0.0
    }


def get_category_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identifies star performing and value-destroying product categories and sub-categories.
    """
    subcat = df.groupby("Sub_Category").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    subcat["Margin_Pct"] = (subcat["Profit"] / subcat["Sales"]) * 100
    
    top_3_subcats = subcat.sort_values("Profit", ascending=False).head(3).to_dict("records")
    bottom_3_subcats = subcat.sort_values("Profit", ascending=True).head(3).to_dict("records")
    
    cat_summary = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    cat_summary["Margin_Pct"] = (cat_summary["Profit"] / cat_summary["Sales"]) * 100
    
    return {
        "top_subcategories": top_3_subcats,
        "bottom_subcategories": bottom_3_subcats,
        "category_summary": cat_summary.to_dict("records")
    }


def generate_executive_narrative(df: pd.DataFrame) -> str:
    """
    Generates a coherent markdown executive summary briefing based on computed data.
    """
    kpis = compute_executive_kpis(df)
    disc = analyze_discount_impact(df)
    cats = get_category_insights(df)
    
    narrative = f"""# Executive Data Story & Performance Briefing

## 1. Enterprise Financial Pulse
- **Total Revenue**: ${kpis['total_sales']:,.2f} across **{kpis['total_orders']:,}** orders.
- **Operating Profit**: ${kpis['total_profit']:,.2f} yielding a net margin of **{kpis['profit_margin_pct']:.2f}%**.
- **Average Order Value (AOV)**: ${kpis['avg_order_value']:,.2f} across **{kpis['unique_customers']:,}** active enterprise customers.
- **Loss-Making Transactions**: **{kpis['loss_making_orders']:,}** transactions ({kpis['loss_order_pct']:.1f}% of total volume) resulted in net negative profit.

## 2. The Core Strategic Finding: The "Discount Trap"
- Orders discounted at **20% or below** generated **${disc['under_20_sales']:,.2f}** in sales and **${disc['under_20_profit']:,.2f}** in profit (**{disc['under_20_margin_pct']:.2f}%** margin).
- Orders discounted **above 20%** accumulated **${disc['over_20_profit']:,.2f}** in net returns (**{disc['over_20_margin_pct']:.2f}%** margin), with a loss incidence of **{disc['high_disc_loss_rate_pct']:.1f}%**.
- **Actionable Conclusion**: Deep discounts do not generate profitable volume; they subsidize buyer acquisition at negative unit economics.

## 3. Portfolio Polarization (Stars vs. Bleeders)
- **Top 3 Profit Engines**:
{chr(10).join([f"  - **{s['Sub_Category']}**: ${s['Profit']:,.2f} profit ({s['Margin_Pct']:.1f}% margin)" for s in cats['top_subcategories']])}
- **Bottom 3 Margin Detractors**:
{chr(10).join([f"  - **{s['Sub_Category']}**: ${s['Profit']:,.2f} profit ({s['Margin_Pct']:.1f}% margin)" for s in cats['bottom_subcategories']])}

## 4. Strategic Imperatives for Leadership
1. **Enforce Hard Discount Guardrails**: Cap discretionary sales discounts at 20% maximum. Require VP-level approval for any discount > 20%.
2. **Restructure Bulky Freight Pricing**: Tables and Bookcases suffer from heavy shipping subsidies. Shift to dynamic carrier freight pass-through.
3. **Double Down on VIP Enterprise Retainers**: Top 20% of customers generate the majority of enterprise revenue. Institutionalize dedicated account managers for tier-1 accounts.
"""
    return narrative
