from config import CSV_FILE, HOST, USER, PASSWORD, DATABASE
from db_utils import import_csv_to_mysql, load_data_from_mysql
from analysis import generate_insights
import visualization as viz

def main():
    while True:
        print("\n=== Sales Dashboard ===")
        print("1. Import CSV to MySQL")
        print("2. Load Data & Analyze (show table head)")
        print("3. Visualize Insights")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            try:
                import_csv_to_mysql(CSV_FILE, HOST, USER, PASSWORD, DATABASE)
            except Exception as e:
                print("Error during import:", e)
        elif choice == "2":
            try:
                df = load_data_from_mysql(HOST, USER, PASSWORD, DATABASE)
                if df.empty:
                    print("Database table is empty.")
                else:
                    print(df.head())
            except Exception as e:
                print("Error loading data:", e)
        elif choice == "3":
            try:
                df = load_data_from_mysql(HOST, USER, PASSWORD, DATABASE)
                insights = generate_insights(df)

                print("\n📊 Top Selling Products:\n", insights['top_products'])
                print("\n📅 Peak Sales Days:\n", insights['peak_days'])
                print("\n📈 Monthly Sales Trend:\n", insights['monthly_sales'])
                print(f"\n💰 Average Order Value (AOV): {insights['avg_order_value']:.2f}")
                print("\n📌 Revenue Contribution by Product (%):\n", insights['revenue_contribution'])

                viz.plot_top_products(insights['top_products'])
                viz.plot_peak_days(insights['peak_days'])
                viz.plot_monthly_sales(insights['monthly_sales'])
                viz.plot_revenue_contribution(insights['revenue_contribution'])

            except Exception as e:
                print("Error analyzing/visualizing:", e)
        elif choice == "4":
            print("👋 Exiting Sales Dashboard. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
