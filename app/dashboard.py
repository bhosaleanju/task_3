"""
Interactive Executive Sales & Profitability Intelligence Dashboard.
Built with Streamlit & Plotly for C-suite decision support.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data
from src.config import COLORS

# Page configuration
st.set_page_config(
    page_title="Executive Sales & Profitability Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
    }
    .kpi-delta-pos {
        font-size: 0.85rem;
        color: #0D9488;
        font-weight: 600;
    }
    .kpi-delta-neg {
        font-size: 0.85rem;
        color: #EF4444;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    return load_data()


df_full = get_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Filter Controls")

min_date = df_full["Order_Date"].min().date()
max_date = df_full["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_regions = st.sidebar.multiselect(
    "Geographic Region",
    options=sorted(df_full["Region"].unique()),
    default=sorted(df_full["Region"].unique())
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df_full["Customer_Segment"].unique()),
    default=sorted(df_full["Customer_Segment"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    options=sorted(df_full["Category"].unique()),
    default=sorted(df_full["Category"].unique())
)

# Apply filters
if len(date_range) == 2:
    start_d, end_d = date_range
    mask = (
        (df_full["Order_Date"].dt.date >= start_d) &
        (df_full["Order_Date"].dt.date <= end_d) &
        (df_full["Region"].isin(selected_regions)) &
        (df_full["Customer_Segment"].isin(selected_segments)) &
        (df_full["Category"].isin(selected_categories))
    )
else:
    mask = (
        (df_full["Region"].isin(selected_regions)) &
        (df_full["Customer_Segment"].isin(selected_segments)) &
        (df_full["Category"].isin(selected_categories))
    )

df = df_full[mask].copy()

# ----------------- HEADER & EXECUTIVE KPIS -----------------
st.markdown('<div class="main-header">Executive Sales & Profitability Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data Visualization & Strategic Decision Support Suite &bull; Multi-Year Commercial Diagnostics</div>', unsafe_allow_html=True)

if len(df) == 0:
    st.warning("No data found matching current filter criteria. Please broaden your selection.")
    st.stop()

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
total_orders = df["Order_ID"].nunique()
active_customers = df["Customer_ID"].nunique()
avg_order_val = total_sales / total_orders if total_orders > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">${total_sales:,.0f}</div>
        <div class="kpi-delta-pos">{total_orders:,} Orders</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    margin_color = "kpi-delta-pos" if profit_margin >= 15 else ("kpi-delta-neg" if profit_margin < 5 else "kpi-delta-pos")
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Net Operating Profit</div>
        <div class="kpi-value">${total_profit:,.0f}</div>
        <div class="{margin_color}">Margin: {profit_margin:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Operating Margin</div>
        <div class="kpi-value">{profit_margin:.1f}%</div>
        <div class="kpi-delta-pos">Target: 15.0%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Active Customers</div>
        <div class="kpi-value">{active_customers:,}</div>
        <div class="kpi-delta-pos">Across {len(selected_regions)} Regions</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Order Value</div>
        <div class="kpi-value">${avg_order_val:,.0f}</div>
        <div class="kpi-delta-pos">Per Transaction</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    " Executive Overview",
    " The Discount Trap",
    " Sub-Category Matrix",
    " Regional Intelligence",
    " Customer Pareto (80/20)",
    " Data Explorer"
])

# ----------------- TAB 1: EXECUTIVE OVERVIEW -----------------
with tab1:
    st.subheader("Multi-Year Commercial Performance Trajectory")
    
    # Monthly aggregation
    monthly = df.groupby("Year_Month").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()
    monthly["Year_Month_Dt"] = pd.to_datetime(monthly["Year_Month"])
    monthly = monthly.sort_values("Year_Month_Dt").reset_index(drop=True)
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Bar(
        x=monthly["Year_Month"],
        y=monthly["Sales"],
        name="Sales Revenue ($)",
        marker_color="#1E3A8A",
        opacity=0.85
    ))
    
    fig_timeline.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Profit"],
        name="Net Operating Profit ($)",
        yaxis="y2",
        line=dict(color="#0D9488", width=3.5),
        mode="lines+markers"
    ))
    
    fig_timeline.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Operational Period (Year-Month)", tickangle=-45),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#F1F5F9"),
        yaxis2=dict(
            title="Net Profit ($)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("#### Revenue by Category")
        cat_agg = df.groupby("Category")["Sales"].sum().reset_index()
        fig_cat = px.pie(
            cat_agg,
            names="Category",
            values="Sales",
            color="Category",
            color_discrete_map={"Technology": "#1E3A8A", "Furniture": "#F59E0B", "Office Supplies": "#0D9488"},
            hole=0.45
        )
        fig_cat.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with c_right:
        st.markdown("#### Sales by Customer Segment")
        seg_agg = df.groupby("Customer_Segment")["Sales"].sum().reset_index()
        fig_seg = px.bar(
            seg_agg,
            x="Customer_Segment",
            y="Sales",
            color="Customer_Segment",
            color_discrete_sequence=["#1E3A8A", "#0284C7", "#38BDF8"],
            text_auto="$,.0f"
        )
        fig_seg.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10), showlegend=False)
        st.plotly_chart(fig_seg, use_container_width=True)

# ----------------- TAB 2: THE DISCOUNT TRAP -----------------
with tab2:
    st.subheader("Pricing Elasticity & Margin Decay Analysis")
    st.markdown("""
    > **Strategic Takeaway**: Transactions with discounts exceeding **20%** systematically result in negative operating profits. 
    > While discounts drive short-term gross volume, they subsidize shipping and COGS at a structural loss.
    """)
    
    # Scatter plot
    sample_vis = df.sample(min(len(df), 1200), random_state=42).copy()
    sample_vis["Status"] = np.where(sample_vis["Profit"] >= 0, "Profitable", "Loss-Making")
    
    fig_scatter = px.scatter(
        sample_vis,
        x=sample_vis["Discount"] * 100,
        y="Profit_Margin_Pct",
        color="Status",
        color_discrete_map={"Profitable": "#0284C7", "Loss-Making": "#EF4444"},
        hover_data=["Order_ID", "Sub_Category", "Sales", "Profit"],
        opacity=0.6,
        labels={"x": "Promotional Discount Rate (%)", "Profit_Margin_Pct": "Profit Margin (%)"}
    )
    
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#0F172A", annotation_text="Break-Even (0% Margin)")
    fig_scatter.add_vline(x=20, line_dash="dot", line_color="#EF4444", annotation_text="Danger Threshold (20%)")
    fig_scatter.update_layout(height=450, template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("###  Interactive Discount Policy Simulator")
    st.markdown("Simulate the enterprise financial impact of enforcing a hard ceiling on sales discounts:")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    with sim_col1:
        cap_pct = st.slider("Simulate Maximum Allowed Discount (%):", min_value=10, max_value=40, value=20, step=5)
        
        # Calculate simulated metrics
        high_disc_subset = df[df["Discount"] > (cap_pct / 100)].copy()
        current_loss = high_disc_subset[high_disc_subset["Profit"] < 0]["Profit"].sum()
        
        # Simulated profit recovery (recovering 70% of loss by avoiding excess markdown)
        recovered_profit = abs(current_loss) * 0.65
        
        st.metric(
            label="Orders Exceeding Proposed Cap",
            value=f"{len(high_disc_subset):,} orders",
            delta=f"{(len(high_disc_subset)/len(df))*100:.1f}% of volume"
        )
        st.metric(
            label="Current Losses in High-Discount Tier",
            value=f"${abs(current_loss):,.0f}",
            delta="-Value Drain",
            delta_color="inverse"
        )
        st.metric(
            label="Estimated Recoverable Annual Profit",
            value=f"+${recovered_profit:,.0f}",
            delta="Margin Expansion",
            delta_color="normal"
        )
        
    with sim_col2:
        tier_agg = df.groupby("Discount_Tier", observed=False).agg({
            "Sales": "sum",
            "Profit": "sum",
            "Order_ID": "count"
        }).reset_index()
        tier_agg["Margin_Pct"] = (tier_agg["Profit"] / tier_agg["Sales"]) * 100
        
        fig_tiers = px.bar(
            tier_agg,
            x="Discount_Tier",
            y="Profit",
            color="Margin_Pct",
            color_continuous_scale="Tealrose",
            text="Margin_Pct",
            title="Profitability by Discount Tier"
        )
        fig_tiers.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_tiers.update_layout(height=340, template="plotly_white")
        st.plotly_chart(fig_tiers, use_container_width=True)

# ----------------- TAB 3: SUB-CATEGORY MATRIX -----------------
with tab3:
    st.subheader("Sub-Category Profit Contribution: Star Performers vs. Loss Leaders")
    
    sub_perf = df.groupby(["Category", "Sub_Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Order_ID": "count"
    }).reset_index()
    sub_perf["Margin_Pct"] = (sub_perf["Profit"] / sub_perf["Sales"]) * 100
    sub_perf = sub_perf.sort_values("Profit", ascending=True)
    
    sub_perf["Color"] = np.where(sub_perf["Profit"] >= 0, "#0D9488", "#EF4444")
    
    fig_sub = go.Figure(go.Bar(
        x=sub_perf["Profit"],
        y=sub_perf["Sub_Category"],
        orientation="h",
        marker_color=sub_perf["Color"],
        text=[f"${p:,.0f} ({m:.1f}%)" for p, m in zip(sub_perf["Profit"], sub_perf["Margin_Pct"])],
        textposition="auto"
    ))
    
    fig_sub.update_layout(
        height=550,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Cumulative Operating Profit ($)", showgrid=True),
        template="plotly_white"
    )
    st.plotly_chart(fig_sub, use_container_width=True)
    
    # Detailed data table
    st.markdown("#### Comprehensive Sub-Category Diagnostics")
    st.dataframe(
        sub_perf[["Category", "Sub_Category", "Sales", "Profit", "Margin_Pct", "Quantity", "Order_ID"]]
        .sort_values("Profit", ascending=False)
        .style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Margin_Pct": "{:+.2f}%",
            "Quantity": "{:,}",
            "Order_ID": "{:,}"
        }),
        use_container_width=True
    )

# ----------------- TAB 4: REGIONAL INTELLIGENCE -----------------
with tab4:
    st.subheader("Regional Performance & Operational Logistics")
    
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        st.markdown("#### Regional Profit Margin Heatmap (%)")
        pivot_sales = df.pivot_table(index="Region", columns="Category", values="Sales", aggfunc="sum")
        pivot_profit = df.pivot_table(index="Region", columns="Category", values="Profit", aggfunc="sum")
        pivot_margin = ((pivot_profit / pivot_sales) * 100).round(1)
        
        fig_heat = px.imshow(
            pivot_margin,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            color_continuous_midpoint=10.0,
            labels=dict(color="Margin (%)")
        )
        fig_heat.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with r_col2:
        st.markdown("#### Shipping Efficiency by Mode")
        ship_perf = df.groupby("Ship_Mode").agg({
            "Shipping_Duration_Days": "mean",
            "Shipping_Cost": "mean",
            "Order_ID": "count"
        }).reset_index()
        
        fig_ship = px.scatter(
            ship_perf,
            x="Shipping_Duration_Days",
            y="Shipping_Cost",
            size="Order_ID",
            color="Ship_Mode",
            text="Ship_Mode",
            color_discrete_sequence=["#1E3A8A", "#0284C7", "#0D9488", "#F59E0B"],
            labels={
                "Shipping_Duration_Days": "Avg Delivery Duration (Days)",
                "Shipping_Cost": "Avg Shipping Cost ($)"
            }
        )
        fig_ship.update_traces(textposition="top center")
        fig_ship.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), template="plotly_white")
        st.plotly_chart(fig_ship, use_container_width=True)

# ----------------- TAB 5: CUSTOMER PARETO ANALYSIS -----------------
with tab5:
    st.subheader("Customer Value Concentration: Pareto Revenue Analysis (80/20 Rule)")
    
    cust_sales = df.groupby(["Customer_ID", "Customer_Name", "Customer_Segment"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order_ID": "count"
    }).sort_values("Sales", ascending=False).reset_index()
    
    cust_sales["Cumulative_Sales"] = cust_sales["Sales"].cumsum()
    cust_sales["Sales_Pct"] = (cust_sales["Cumulative_Sales"] / cust_sales["Sales"].sum()) * 100
    cust_sales["Customer_Pct"] = ((cust_sales.index + 1) / len(cust_sales)) * 100
    
    idx_20 = (cust_sales["Customer_Pct"] - 20).abs().idxmin()
    rev_at_20 = cust_sales["Sales_Pct"].iloc[idx_20]
    
    fig_pareto = go.Figure()
    
    fig_pareto.add_trace(go.Scatter(
        x=cust_sales["Customer_Pct"],
        y=cust_sales["Sales_Pct"],
        mode="lines",
        line=dict(color="#1E3A8A", width=3),
        name="Cumulative Revenue Share (%)",
        fill="tozeroy",
        fillcolor="rgba(30, 58, 138, 0.08)"
    ))
    
    fig_pareto.add_trace(go.Scatter(
        x=[0, 100],
        y=[0, 100],
        mode="lines",
        line=dict(color="#94A3B8", dash="dash"),
        name="Equality Baseline"
    ))
    
    fig_pareto.add_vline(x=20, line_dash="dot", line_color="#F59E0B")
    fig_pareto.add_hline(y=rev_at_20, line_dash="dot", line_color="#F59E0B")
    
    fig_pareto.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Cumulative Share of Customer Base (%)"),
        yaxis=dict(title="Cumulative Share of Total Revenue (%)"),
        annotations=[
            dict(
                x=20,
                y=rev_at_20,
                text=f"Top 20% Accounts = {rev_at_20:.1f}% Revenue",
                showarrow=True,
                arrowhead=2,
                ax=60,
                ay=-40,
                bgcolor="#FFFBEB",
                bordercolor="#F59E0B"
            )
        ],
        template="plotly_white"
    )
    st.plotly_chart(fig_pareto, use_container_width=True)
    
    st.markdown("#### Top 10 High-Value Enterprise Accounts")
    st.dataframe(
        cust_sales.head(10)[["Customer_ID", "Customer_Name", "Customer_Segment", "Sales", "Profit", "Order_ID"]]
        .style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Order_ID": "{:,}"
        }),
        use_container_width=True
    )

# ----------------- TAB 6: DATA EXPLORER -----------------
with tab6:
    st.subheader("Raw & Filtered Transactional Dataset")
    st.write(f"Displaying **{len(df):,}** records matching active filters.")
    
    st.dataframe(df, use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=" Download Filtered Dataset (CSV)",
        data=csv_bytes,
        file_name="executive_filtered_sales.csv",
        mime="text/csv"
    )
