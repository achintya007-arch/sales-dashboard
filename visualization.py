import matplotlib.pyplot as plt

def plot_top_products(top_products):
    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(top_products.index, top_products.values, 
                  color=['#4CAF50','#2196F3','#FFC107','#FF5722','#9C27B0'])
    ax.set_title("Top Selling Products", fontsize=14, fontweight='bold')
    ax.set_xlabel("Product", fontsize=12)
    ax.set_ylabel("Total Sales", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{bar.get_height():.0f}", ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    return fig

def plot_peak_days(peak_days):
    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(peak_days.index.astype(str), peak_days.values, color='#FF9800')
    ax.set_title("Top Sales Days", fontsize=14, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Total Sales", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{bar.get_height():.0f}", ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    return fig

def plot_monthly_sales(monthly_sales):
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(monthly_sales.index.astype(str), monthly_sales.values, 
            marker='o', color='#4CAF50', linewidth=2)
    ax.set_title("Monthly Sales Trend", fontsize=14, fontweight='bold')
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Sales", fontsize=12)
    ax.grid(linestyle='--', alpha=0.7)
    for x, y in zip(monthly_sales.index.astype(str), monthly_sales.values):
        ax.text(x, y, f"{y:.0f}", ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    return fig

def plot_revenue_contribution(revenue_contribution):
    fig, ax = plt.subplots(figsize=(6,6))
    colors = ['#4CAF50','#2196F3','#FFC107','#FF5722',
              '#9C27B0','#00BCD4','#E91E63']
    revenue_contribution.plot(kind='pie', autopct='%1.1f%%',
                              startangle=90, colors=colors,
                              textprops={'fontsize': 10}, ax=ax)
    ax.set_title("Revenue Contribution by Product", fontsize=14, fontweight='bold')
    ax.set_ylabel("")
    return fig