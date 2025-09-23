import pandas as pd

def generate_insights(df):
    df['total'] = df['quantity'] * df['price']

    insights = {}
    insights['top_products'] = df.groupby('product_name')['total'].sum().sort_values(ascending=False).head(5)
    insights['peak_days'] = df.groupby('order_date')['total'].sum().sort_values(ascending=False).head(5)

    df['month'] = pd.to_datetime(df['order_date']).dt.to_period('M')
    insights['monthly_sales'] = df.groupby('month')['total'].sum()

    insights['total_revenue'] = df['total'].sum()
    insights['total_orders'] = df['order_id'].nunique()
    insights['avg_order_value'] = insights['total_revenue'] / insights['total_orders']
    insights['revenue_contribution'] = (df.groupby('product_name')['total'].sum() / insights['total_revenue'] * 100).sort_values(ascending=False)

    return insights