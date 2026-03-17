import streamlit as st
import pandas as pd
from db_utils import import_csv_to_mysql, load_data_from_mysql
from analysis import generate_insights
import visualization as viz

CSV_FILE = "sales.csv"

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container { padding: 1rem 2rem; }
.metric-container {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stMetric { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Navigation")
menu = ["📈 Overview & Insights", "📋 View Data", "🏠 Import CSV"]
choice = st.sidebar.radio("Go to", menu)

st.title("📊 Sales Analytics Dashboard")
st.markdown("Analyze your sales data quickly with KPIs, trends, and visual insights.")

@st.cache_data
def get_data():
    try:
        df = load_data_from_mysql()   # ⭐ UPDATED
        return df
    except Exception:
        return pd.DataFrame()

df = get_data()

# ================= Overview =================
if choice == "📈 Overview & Insights":
    st.header("📊 Sales Overview & KPIs")

    if df.empty:
        st.warning("⚠️ No data available. Please import CSV first.")

        total_revenue = 50000
        total_orders = 120
        avg_order_value = total_revenue / total_orders
        top_products = pd.Series([30, 20, 15], index=["Product A", "Product B", "Product C"])
        monthly_sales = pd.Series(
            [4000, 5000, 6000, 4500, 7000],
            index=pd.date_range("2025-01-01", periods=5, freq='M')
        )
    else:
        insights = generate_insights(df)
        total_revenue = insights['total_revenue']
        total_orders = insights['total_orders']
        avg_order_value = insights['avg_order_value']
        top_products = insights['top_products']
        monthly_sales = insights['monthly_sales']

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("🛒 Total Orders", f"{total_orders}")
    col3.metric("📦 Avg Order Value", f"₹{avg_order_value:,.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top Selling Products")
        st.bar_chart(top_products)

        st.subheader("📅 Peak Sales Days")
        if not df.empty:
            st.bar_chart(insights['peak_days'])
        else:
            st.bar_chart([5, 10, 7])

    with col2:
        st.subheader("📈 Monthly Sales Trend")
        st.line_chart(monthly_sales)

        st.subheader("Revenue Contribution by Product")
        if not df.empty:
            fig = viz.plot_revenue_contribution(insights['revenue_contribution'])
            st.pyplot(fig)

# ================= View Data =================
elif choice == "📋 View Data":
    st.header("👀 Sales Data Preview")
    if df.empty:
        st.warning("⚠️ No data found in the database. Please import CSV first.")
    else:
        st.dataframe(df.head(50), use_container_width=True)
        st.markdown("### Summary Statistics")
        st.dataframe(df.describe())

# ================= Import CSV =================
elif choice == "🏠 Import CSV":
    st.header("📥 Import CSV to MySQL")

    if st.button("🚀 Import Now"):
        try:
            import_csv_to_mysql(CSV_FILE)   # ⭐ UPDATED
            st.success("✅ Data imported successfully into MySQL!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")