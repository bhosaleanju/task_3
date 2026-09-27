"""
Configuration module for Data Visualization & Storytelling Suite.
Defines styling themes, corporate palettes, and directory paths.
Adheres to Edward Tufte and Stephen Few data visualization principles:
- High data-ink ratio
- Intentional color hierarchy (not decorative rainbow palettes)
- Clean, minimal chartjunk
- Readable typography and subtle gridlines
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Directory Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "ecommerce_sales_data.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "ecommerce_cleaned.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Ensure essential output directories exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# Executive Color Palette (High contrast, colorblind-friendly accents)
COLORS = {
    "primary": "#1E3A8A",       # Deep Navy - Core metric / baseline
    "secondary": "#0284C7",     # Ocean Blue - Secondary metric
    "positive": "#0D9488",      # Teal / Green - Profit / Growth
    "negative": "#EF4444",      # Coral Red - Loss / Critical alert
    "neutral": "#64748B",       # Slate Grey - Contextual baseline
    "neutral_light": "#F1F5F9", # Light slate - Backgrounds / cards
    "warning": "#F59E0B",       # Amber - Caution / Watchlist
    "dark_text": "#0F172A",     # Slate 900 - High legibility text
    "muted_text": "#475569",    # Slate 600 - Subtitles & captions
    "grid": "#E2E8F0"           # Slate 200 - Soft structural guides
}

# Qualitative Category Colors
CATEGORY_PALETTE = {
    "Technology": "#1E3A8A",     # Navy
    "Furniture": "#F59E0B",      # Amber
    "Office Supplies": "#0D9488" # Teal
}

# Diverging Palette for Profitability
PROFIT_PALETTE = [COLORS["negative"], "#FCA5A5", "#E2E8F0", "#99F6E4", COLORS["positive"]]


def apply_plot_theme():
    """
    Applies an executive publication-grade theme to Matplotlib and Seaborn.
    Sets clean typography, soft gridlines, and uncluttered spines.
    """
    # Base Seaborn style
    sns.set_theme(style="white", font="sans-serif")
    
    # Custom Matplotlib rcParams for high-fidelity rendering
    plt.rcParams.update({
        # Figure properties
        "figure.dpi": 120,
        "figure.facecolor": "#FFFFFF",
        "figure.edgecolor": "#FFFFFF",
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.facecolor": "#FFFFFF",
        "savefig.transparent": False,
        
        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica Neue", "Arial"],
        "text.color": COLORS["dark_text"],
        "axes.labelcolor": COLORS["dark_text"],
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlepad": 14,
        "axes.labelsize": 11,
        "axes.labelweight": "medium",
        "axes.labelpad": 8,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color": COLORS["muted_text"],
        "ytick.color": COLORS["muted_text"],
        
        # Spines and Grid
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.edgecolor": "#CBD5E1",
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": COLORS["grid"],
        "grid.linestyle": "--",
        "grid.linewidth": 0.7,
        "grid.alpha": 0.8,
        
        # Legend
        "legend.frameon": False,
        "legend.fontsize": 10,
        "legend.title_fontsize": 11,
    })


def save_figure(fig, filename: str, dpi: int = 300):
    """
    Saves a Matplotlib figure to the figures directory with standardized settings.
    
    Args:
        fig: Matplotlib figure object
        filename: Target image filename (e.g., '01_sales_trends.png')
        dpi: Resolution (default: 300 DPI for publication quality)
    """
    out_path = FIGURES_DIR / filename
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f" Saved figure: {out_path}")
    return out_path
