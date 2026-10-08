from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data" / "cleaned"

st.set_page_config(
    page_title="Olist | E-commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Loading the cleaned Olist data…")
def load_data():
    orders = pd.read_csv(DATA_DIR / "olist_orders_clean.csv", parse_dates=["order_purchase_timestamp"])
    items = pd.read_csv(DATA_DIR / "olist_order_items_clean.csv")
    customers = pd.read_csv(DATA_DIR / "olist_customers_clean.csv")
    products = pd.read_csv(DATA_DIR / "olist_products_clean.csv")
    translations = pd.read_csv(DATA_DIR / "product_category_name_translation_clean.csv")

    items = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    items = items.merge(translations, on="product_category_name", how="left")
    items["category"] = items["product_category_name_english"].fillna(
        items["product_category_name"]
    ).fillna("Uncategorized")

    customer_counts = customers.groupby("customer_unique_id")["customer_id"].nunique()
    repeat_customers = set(customer_counts[customer_counts > 1].index)
    customer_lookup = customers[["customer_id", "customer_unique_id"]].drop_duplicates("customer_id")
    orders = orders.merge(customer_lookup, on="customer_id", how="left")
    orders["is_repeat_customer"] = orders["customer_unique_id"].isin(repeat_customers)

    return orders, items


st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1440px;}
    [data-testid="stMetric"] {background: #ffffff; border: 1px solid #e8edf3;
        padding: 18px 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(20, 40, 70, .04);}
    [data-testid="stMetricLabel"] {color: #607086;}
    [data-testid="stMetricValue"] {color: #14253d;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛍️ Olist E-commerce Analytics")
st.caption("A clear view of sales, customers, and order performance across the Olist marketplace.")

try:
    orders, items = load_data()
except FileNotFoundError as error:
    st.error(f"A required cleaned CSV is missing: `{error.filename}`. Check the `data/cleaned` folder.")
    st.stop()

if orders.empty:
    st.warning("The orders file has no rows to display.")
    st.stop()

min_date = orders["order_purchase_timestamp"].min().date()
max_date = orders["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.header("Dashboard filters")
    st.caption("Choose a purchase date range to update the overview.")
    selected_dates = st.date_input(
        "Purchase date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    st.divider()
    st.caption("Data source: cleaned Olist CSV files")

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

date_column = orders["order_purchase_timestamp"].dt.date
filtered_orders = orders[date_column.between(start_date, end_date)].copy()
filtered_items = items[items["order_id"].isin(filtered_orders["order_id"])].copy()

if filtered_orders.empty:
    st.info("No orders fall within this date range. Choose a wider range in the sidebar.")
    st.stop()

revenue = filtered_items["price"].sum()
order_count = filtered_orders["order_id"].nunique()
customer_count = filtered_orders["customer_unique_id"].nunique()
average_order_value = revenue / order_count if order_count else 0
repeat_rate = filtered_orders.loc[filtered_orders["is_repeat_customer"], "customer_unique_id"].nunique()
repeat_rate = repeat_rate / customer_count if customer_count else 0
cancel_rate = filtered_orders["order_status"].eq("canceled").mean()

st.subheader("Overview")
metric_columns = st.columns(5)
metric_columns[0].metric("Product revenue", f"R$ {revenue:,.0f}")
metric_columns[1].metric("Orders", f"{order_count:,}")
metric_columns[2].metric("Customers", f"{customer_count:,}")
metric_columns[3].metric("Average order value", f"R$ {average_order_value:,.2f}")
metric_columns[4].metric("Repeat customer rate", f"{repeat_rate:.1%}")

completed_count = filtered_orders["order_status"].eq("delivered").sum()
st.caption(
    f"{start_date:%d %b %Y} – {end_date:%d %b %Y} · "
    f"{completed_count:,} delivered orders · {cancel_rate:.1%} cancellation rate"
)

monthly_orders = filtered_orders.assign(
    month=filtered_orders["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
)
monthly_revenue = filtered_items.merge(
    filtered_orders[["order_id", "order_purchase_timestamp"]], on="order_id", how="inner"
)
monthly_revenue["month"] = monthly_revenue["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
revenue_trend = monthly_revenue.groupby("month")["price"].sum().rename("Revenue")
orders_trend = monthly_orders.groupby("month")["order_id"].nunique().rename("Orders")
trend = pd.concat([revenue_trend, orders_trend], axis=1).fillna(0).sort_index()

left, right = st.columns([1.65, 1])
with left:
    st.markdown("#### Sales over time")
    if trend.empty:
        st.info("No sales data is available for this period.")
    else:
        st.line_chart(trend, height=330, color=["#2563eb", "#f59e0b"])
with right:
    st.markdown("#### Order status")
    status_counts = filtered_orders["order_status"].value_counts().rename_axis("Status").to_frame("Orders")
    st.bar_chart(status_counts, height=330, color="#0f766e")

bottom_left, bottom_right = st.columns([1.35, 1])
with bottom_left:
    st.markdown("#### Top product categories")
    category_sales = (
        filtered_items.groupby("category")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .rename("Product revenue (R$)")
    )
    if category_sales.empty:
        st.info("No product category data is available for this period.")
    else:
        st.bar_chart(category_sales, height=340, color="#7c3aed", horizontal=True)
with bottom_right:
    st.markdown("#### At a glance")
    st.metric("Delivered orders", f"{completed_count:,}")
    st.metric("Canceled orders", f"{filtered_orders['order_status'].eq('canceled').sum():,}")
    st.markdown(
        "Revenue reflects item prices from the order items file; freight and payment adjustments are excluded."
    )

st.divider()
st.caption("Built with Python, pandas, and Streamlit · Olist Brazilian e-commerce dataset")
