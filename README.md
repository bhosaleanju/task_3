# Executive Sales & Profitability Intelligence: Data Visualization Suite (Task 3)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C.svg)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12%2B-4C72B0.svg)](https://seaborn.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com)
[![Visual Design](https://img.shields.io/badge/Design_Principles-Edward_Tufte-emerald.svg)](#visual-design-philosophy)

Transforming raw transactional retail data into **impactful executive visualizations, interactive dashboards, and strategic business stories**.

---

## Executive Overview

In corporate analytics, raw data alone does not drive change—**visual clarity does**. This project transforms over 3,200 multi-year retail transactions ($4.34M in revenue) into a cohesive visual intelligence suite that uncovers hidden margin leaks, evaluates promotional price elasticity, and diagnoses geographic and portfolio imbalances.

### Key Business Diagnostics Uncovered:
1. **The "Discount Trap" (Critical Inflection at 20%)**: Sales discounted at $\le 20\%$ deliver healthy operating margins ($+24\%$). In contrast, promotions exceeding $20\%$ plunge into net negative unit economics due to unrecovered freight and handling.
2. **Portfolio Polarization**: High-margin categories (Copiers, Phones, Accessories) subsidize heavy margin bleeders (Tables, Bookcases) which suffer from excessive freight and clearance markdowns.
3. **Regional Freight Friction**: Furniture operations in the Central ($-8.4\%$) and Southern ($-6.2\%$) territories operate at a loss due to shipping distance subsidies.
4. **Pareto Customer Concentration**: The top $20\%$ of customer accounts generate $68.4\%$ of total enterprise revenue, emphasizing the need for high-touch account retention.

---

## Visual Gallery & Publication Figures

All static figures are rendered at **300 DPI publication quality** adhering to Edward Tufte and Stephen Few design standards (high data-ink ratio, zero chartjunk, direct labeling, and corporate palette hierarchy).

| Figure | Description | Preview |
| :--- | :--- | :--- |
| **01. Revenue Trajectory** | Dual-axis longitudinal trajectory tracking monthly sales and operating margins with seasonal holiday peak callouts. | `reports/figures/01_sales_profit_trends.png` |
| **02. The Discount Trap** | Price elasticity scatter and polynomial regression highlighting the 20% discount danger zone. | `reports/figures/02_discount_profit_impact.png` |
| **03. Sub-Category Matrix** | Horizontal diverging bar chart isolating star profit engines from margin detractors. | `reports/figures/03_category_profitability_diverging.png` |
| **04. Regional Heatmap** | Geographic and category profit margin cross-tabulation with annotated percentages. | `reports/figures/04_regional_performance_heatmap.png` |
| **05. Customer Pareto** | Cumulative revenue concentration curve demonstrating the 80/20 distribution. | `reports/figures/05_pareto_customer_distribution.png` |

---

## Project Architecture

```text
tsak 3/
├── data/
│   ├── raw/
│   │   └── ecommerce_sales_data.csv          # Multi-year transactional retail dataset
│   └── processed/
│       └── ecommerce_cleaned.csv             # Feature-engineered analytical dataset
├── notebooks/
│   └── 01_executive_data_story.ipynb        # Comprehensive storytelling Jupyter Notebook
├── src/
│   ├── __init__.py
│   ├── config.py                             # Tufte/Few styling themes, corporate palettes, rcParams
│   ├── data_loader.py                        # Data ingestion, synthetic simulation, feature engineering
│   ├── visualizer.py                         # 300-DPI publication plotting engine (Matplotlib/Seaborn)
│   └── storytelling.py                       # Automated narrative and KPI extraction engine
├── app/
│   └── dashboard.py                          # Modern interactive Streamlit & Plotly executive dashboard
├── reports/
│   ├── figures/                              # High-resolution (300 DPI) chart artifacts (.png)
│   ├── EXECUTIVE_SUMMARY.md                  # C-level decision memo with strategic recommendations
│   └── interactive_dashboard.html            # Standalone, zero-dependency interactive HTML dashboard
├── generate_all_reports.py                   # Automated end-to-end master pipeline script
├── requirements.txt                          # Project dependencies
└── README.md                                 # Portfolio documentation
```

---

## Visual Design Philosophy

This project rejects decorative "chartjunk" (garish 3D charts, superfluous rainbow palettes, heavy gridlines) in favor of **clarity and cognitive ergonomics**:
- **High Data-to-Ink Ratio**: Every visual element (line, tick, label) conveys meaningful business information.
- **Intentional Color Hierarchy**: Navy (`#1E3A8A`) for base metrics, Teal (`#0D9488`) for positive profit, and Coral Red (`#EF4444`) strictly reserved for losses and critical risk thresholds.
- **Direct Labeling**: Eliminates eye-travel by placing values and percentage margins directly at the endpoints of bars and peaks.
- **Contextual Annotations**: Incorporates narrative callout boxes directly within visual artifacts to guide stakeholder interpretation.

---

## Quickstart & Execution

### 1. Environment Installation
Ensure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Run the Automated Pipeline
Generates the dataset, computes executive metrics, exports all 5 high-resolution figures, and produces the executive summary:
```bash
python generate_all_reports.py
```

### 3. Launch the Interactive Streamlit Dashboard
Experience real-time filtering, dynamic KPI cards, and the interactive **Discount Policy Simulator**:
```bash
streamlit run app/dashboard.py
```

### 4. Explore the Jupyter Storytelling Notebook
Open `notebooks/01_executive_data_story.ipynb` in VS Code or JupyterLab:
```bash
jupyter notebook notebooks/01_executive_data_story.ipynb
```

### 5. View the Standalone HTML Dashboard
Double-click `reports/interactive_dashboard.html` to open an interactive, zero-dependency dashboard in any web browser—ideal for sharing with recruiters and stakeholders!

---

## Strategic Recommendations for Leadership

| Strategic Pillar | Actionable Initiative | Expected Commercial Impact |
| :--- | :--- | :--- |
| **Pricing Governance** | Enforce a strict 20% discount ceiling; require executive approval for exceptions. | Recover **+$120K+** in annual gross profit. |
| **Freight Restructuring** | Transition bulky Furniture (Tables/Bookcases) to dynamic freight pass-through. | Eliminate **-$49K** in unrecovered shipping subsidies. |
| **Portfolio Focus** | Reallocate marketing capital toward Copiers, Phones, and Accessories. | Accelerate high-margin category growth by **18%**. |
| **Account Retention** | Deploy dedicated Key Account Managers for the top 20% customer cohort. | Protect **$2.97M** (68.4%) in enterprise revenue base. |

---

## License & Attribution
Developed as a portfolio-grade demonstration of **Advanced Data Visualization & Business Analytics**. Distributed under the MIT License.
