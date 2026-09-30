import os
import time
import pandas as pd
import streamlit as st
import altair as alt

from dotenv import load_dotenv
from google import genai
from google.genai import types

from business_data import (
    get_sales_summary,
    get_inventory_summary,
    get_monthly_revenue,
    get_category_revenue,
    get_top_selling_products,
)


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Business Analyst Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Business Analyst Assistant")
st.write(
    "Ask questions about your clothing sales, profitability, "
    "products, and inventory."
)


# ============================================================
# 2. LOAD GEMINI API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning(
        "Gemini API key not found. The app will use SQL-based "
        "answers for supported questions."
    )
    client = None
else:
    client = genai.Client(api_key=api_key)


# ============================================================
# 3. LOAD BUSINESS DATA FROM SQL SERVER
# ============================================================

try:
    sales = get_sales_summary()
    inventory = get_inventory_summary()
    monthly_revenue = get_monthly_revenue()
    category_revenue = get_category_revenue()
    top_products = get_top_selling_products()

except Exception as error:
    st.error(f"Could not retrieve data from SQL Server: {error}")
    st.stop()

st.success("Connected to SQL Server — current business data loaded.")
# ============================================================
# BUSINESS PERFORMANCE DASHBOARD
# ============================================================

st.divider()
st.header("📈 Business Performance Dashboard")

# Calculate total remaining inventory
total_stock = sum(
    item["remaining_stock"] for item in inventory
)

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{sales['total_revenue']:,.2f}"
    )

with col2:
    st.metric(
        "Gross Profit",
        f"₹{sales['gross_profit']:,.2f}"
    )

with col3:
    st.metric(
        "Completed Orders",
        f"{sales['total_orders']:,}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Units Sold",
        f"{sales['total_units_sold']:,}"
    )

with col5:
    st.metric(
        "Total Product Cost",
        f"₹{sales['total_cost']:,.2f}"
    )

with col6:
    st.metric(
        "Remaining Inventory",
        f"{total_stock:,} pieces"
    )

st.divider()

# Monthly Revenue Chart
st.subheader("📅 Monthly Revenue")

if monthly_revenue:
    monthly_df = pd.DataFrame(monthly_revenue)

    # Set calendar order explicitly
    month_order = [
        "January 2025",
        "February 2025",
        "March 2025"
    ]

    monthly_chart = alt.Chart(monthly_df).mark_bar().encode(
        x=alt.X(
    "month:N",
    sort=month_order,
    title="Month",
    axis=alt.Axis(labelAngle=0, labelLimit=150)
),
        y=alt.Y(
            "revenue:Q",
            title="Revenue (₹)"
        ),
        tooltip=[
            alt.Tooltip("month:N", title="Month"),
            alt.Tooltip("revenue:Q", title="Revenue", format=",.2f")
        ]
    )

    st.altair_chart(monthly_chart, use_container_width=True)

else:
    st.info("No monthly revenue data available.")

# Category Revenue Chart
st.subheader("👕 Revenue by Product Category")

if category_revenue:
    category_df = pd.DataFrame(category_revenue)
    st.bar_chart(
        category_df,
        x="category",
        y="revenue"
    )
else:
    st.info("No category revenue data available.")

# Top-Selling Products Chart
st.subheader("🏆 Top-Selling Products")

if top_products:
    products_df = pd.DataFrame(top_products)
    st.bar_chart(
        products_df,
        x="product",
        y="units_sold"
    )
else:
    st.info("No product sales data available.")

# Inventory Chart
st.subheader("📦 Remaining Stock by Product")

if inventory:
    inventory_df = pd.DataFrame(inventory)
    st.bar_chart(
        inventory_df,
        x="product",
        y="remaining_stock"
    )
else:
    st.info("No inventory data available.")
# ============================================================
# AUTOMATIC BUSINESS INSIGHTS
# ============================================================

st.divider()
st.header("💡 Automatic Business Insights")

# Highest revenue month
if monthly_revenue:
    highest_month = max(
        monthly_revenue,
        key=lambda item: item["revenue"]
    )

    st.info(
        f"📅 **Highest Revenue Month:** {highest_month['month']} "
        f"with ₹{highest_month['revenue']:,.2f} in revenue."
    )

# Highest revenue category
if category_revenue:
    highest_category = max(
        category_revenue,
        key=lambda item: item["revenue"]
    )

    st.info(
        f"👕 **Leading Category by Revenue:** "
        f"{highest_category['category']} "
        f"with ₹{highest_category['revenue']:,.2f}."
    )

# Top-selling product
if top_products:
    best_product = top_products[0]

    st.info(
        f"🏆 **Top-Selling Product:** {best_product['product']} "
        f"with {best_product['units_sold']} units sold."
    )

# Low-stock products
low_stock_items = [
    item for item in inventory
    if item["remaining_stock"] <= 80
]

if low_stock_items:
    low_stock_names = ", ".join(
        f"{item['product']} ({item['remaining_stock']} pieces)"
        for item in low_stock_items
    )

    st.warning(
        f"⚠️ **Low-Stock Alert:** {low_stock_names}. "
        "These products have 80 pieces or fewer remaining."
    )
else:
    st.success("No products currently meet the low-stock threshold.")
st.divider()
st.header("💬 Ask Your Business Analyst")

# ============================================================
# 4. PREPARE VERIFIED DATA FOR GEMINI
# ============================================================

inventory_text = "\n".join(
    f"- {item['product']}: {item['remaining_stock']} pieces remaining"
    for item in inventory
)

monthly_text = "\n".join(
    f"- {item['month']}: ₹{item['revenue']:,.2f}"
    for item in monthly_revenue
)

category_text = "\n".join(
    f"- {item['category']}: ₹{item['revenue']:,.2f}"
    for item in category_revenue
)

top_products_text = "\n".join(
    f"- {item['product']}: {item['units_sold']} units sold, "
    f"revenue ₹{item['revenue']:,.2f}"
    for item in top_products
)

business_context = f"""
VERIFIED CLOTHING RETAIL DATA FROM SQL SERVER

SALES SUMMARY:
- Total revenue: ₹{sales['total_revenue']:,.2f}
- Total cost: ₹{sales['total_cost']:,.2f}
- Gross profit: ₹{sales['gross_profit']:,.2f}
- Total units sold: {sales['total_units_sold']}
- Completed orders: {sales['total_orders']}

MONTHLY REVENUE:
{monthly_text}

CATEGORY-WISE REVENUE:
{category_text}

TOP-SELLING PRODUCTS:
{top_products_text}

CURRENT INVENTORY:
{inventory_text}

LOW STOCK RULE:
Products with 80 pieces or fewer are considered low stock.

These figures were retrieved from the connected SQL Server database.
Sales figures include completed orders.
"""


# ============================================================
# 5. GEMINI AI FUNCTION WITH RETRIES
# ============================================================

def ask_gemini(question):

    if client is None:
        raise RuntimeError("Gemini API key is not configured.")

    prompt = f"""
You are an AI Business Analyst Assistant for a clothing retail business.

Use only the verified business data below to answer the user's question.

BUSINESS DATA:
{business_context}

USER QUESTION:
{question}

INSTRUCTIONS:
- Answer clearly and professionally in simple language.
- Use only the supplied data for business figures.
- Do not invent numbers, dates, or facts.
- Show calculations when useful.
- If the data does not contain the answer, explain what is missing.
- Distinguish confirmed facts from possible explanations.
- Do not claim to have queried or modified the database.
- Do not generate or execute SQL commands.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=600
                )
            )

            if not response.text:
                return "Gemini returned an empty response. Please try again."

            return response.text

        except Exception as error:
            error_message = str(error).lower()

            # Do not retry quota-exhaustion errors.
            quota_error = (
                "429" in error_message
                or "resource_exhausted" in error_message
                or "quota" in error_message
            )

            if quota_error:
                raise

            # Retry temporary availability errors.
            temporary_error = (
                "503" in error_message
                or "unavailable" in error_message
                or "high demand" in error_message
            )

            if temporary_error and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise


# ============================================================
# 6. SQL-BASED FALLBACK ANSWERS
# ============================================================

def get_sql_fallback_answer(question):

    q = question.lower()

    # --------------------------------------------------------
    # Gross profit
    # --------------------------------------------------------

    if "gross profit" in q or "profit" in q:

        return (
            f"**Total gross profit: ₹{sales['gross_profit']:,.2f}**\n\n"
            f"- Revenue: ₹{sales['total_revenue']:,.2f}\n"
            f"- Cost: ₹{sales['total_cost']:,.2f}\n\n"
            "Gross profit = Revenue − Cost."
        )

    # --------------------------------------------------------
    # Total cost
    # --------------------------------------------------------

    if "total cost" in q or "cost of goods" in q:

        return (
            f"Total product cost: ₹{sales['total_cost']:,.2f}"
        )

    # --------------------------------------------------------
    # Monthly revenue
    # --------------------------------------------------------

    if "month" in q or "monthly" in q:

        if not monthly_revenue:
            return "No monthly revenue records were returned."

        monthly_list = "\n".join(
            f"- {item['month']}: ₹{item['revenue']:,.2f}"
            for item in monthly_revenue
        )

        if (
            "highest" in q
            or "most" in q
            or "maximum" in q
            or "best" in q
        ):
            highest_month = max(
                monthly_revenue,
                key=lambda item: item["revenue"]
            )

            return (
                f"**Highest revenue month: {highest_month['month']}** "
                f"with ₹{highest_month['revenue']:,.2f}.\n\n"
                f"Monthly revenue:\n{monthly_list}"
            )

        return f"**Monthly revenue:**\n\n{monthly_list}"

    # --------------------------------------------------------
    # Category revenue
    # --------------------------------------------------------

    if "categor" in q:

        if not category_revenue:
            return "No category revenue records were returned."

        matching_categories = [
            item for item in category_revenue
            if item["category"].lower() in q
        ]

        if matching_categories:
            item = matching_categories[0]

            return (
                f"**{item['category']} revenue: "
                f"₹{item['revenue']:,.2f}**"
            )

        category_list = "\n".join(
            f"- {item['category']}: ₹{item['revenue']:,.2f}"
            for item in category_revenue
        )

        return f"**Category-wise revenue:**\n\n{category_list}"

    # --------------------------------------------------------
    # Top-selling products
    # --------------------------------------------------------

    if (
        "top sell" in q
        or "best sell" in q
        or "most sold" in q
        or "popular product" in q
        or "sold the most" in q
        or "most units" in q
        or "highest quantity" in q
        or "highest number of units" in q
        or "which product" in q
        or "what product" in q
    ):

        if not top_products:
            return "No product sales records were returned."

        first_product = top_products[0]

        product_list = "\n".join(
            f"- {item['product']}: {item['units_sold']} units sold, "
            f"revenue ₹{item['revenue']:,.2f}"
            for item in top_products
        )

        return (
            f"**Most units sold: {first_product['product']}** "
            f"({first_product['units_sold']} units).\n\n"
            f"Top-selling products:\n{product_list}"
        )
    # --------------------------------------------------------
    # Low stock
    # --------------------------------------------------------

    if "low stock" in q or "lowest stock" in q:

        if not inventory:
            return "No inventory records were returned."

        lowest_item = min(
            inventory,
            key=lambda item: item["remaining_stock"]
        )

        low_stock_items = [
            item for item in inventory
            if item["remaining_stock"] <= 80
        ]

        if low_stock_items:
            low_stock_list = "\n".join(
                f"- {item['product']}: {item['remaining_stock']} pieces"
                for item in low_stock_items
            )
        else:
            low_stock_list = "No products currently meet the low-stock rule."

        return (
            f"**Lowest remaining stock: {lowest_item['product']}** "
            f"({lowest_item['remaining_stock']} pieces).\n\n"
            f"Low-stock products (80 pieces or fewer):\n{low_stock_list}"
        )

     # --------------------------------------------------------
    # Inventory
    # --------------------------------------------------------

    if "inventory" in q or "stock" in q:

        if not inventory:
            return "No inventory records were returned."

        total_remaining_stock = sum(
            item["remaining_stock"] for item in inventory
        )

        if (
            "total" in q
            or "overall" in q
            or "in total" in q
        ):
            return (
                f"**Total remaining inventory: "
                f"{total_remaining_stock} pieces**"
            )

        inventory_list = "\n".join(
            f"- {item['product']}: "
            f"{item['remaining_stock']} pieces remaining"
            for item in inventory
        )

        return f"**Current inventory:**\n\n{inventory_list}"

    # --------------------------------------------------------
    # Units sold
    # --------------------------------------------------------

    if (
        "unit" in q
        or "quantity sold" in q
        or "how many sold" in q
    ):

        return (
            f"Total units sold: {sales['total_units_sold']}"
        )

    # --------------------------------------------------------
    # Order count
    # --------------------------------------------------------

    if "order" in q:

        return (
            f"Total completed orders: {sales['total_orders']}"
        )

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    if "revenue" in q or "sales amount" in q:

        return (
            f"Total revenue: ₹{sales['total_revenue']:,.2f}\n\n"
            f"Completed orders: {sales['total_orders']}"
        )

    return None


# ============================================================
# 7. CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# 8. CHAT INPUT AND RESPONSE
# ============================================================

prompt = st.chat_input("Ask a business question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your business data..."):

            try:
                answer = ask_gemini(prompt)
                st.markdown(answer)

            except Exception as error:

                error_message = str(error).lower()

                quota_error = (
                    "429" in error_message
                    or "resource_exhausted" in error_message
                    or "quota" in error_message
                )

                temporary_error = (
                    "503" in error_message
                    or "unavailable" in error_message
                    or "high demand" in error_message
                )

                if quota_error or temporary_error:

                    if quota_error:
                        st.warning(
                            "Gemini API quota has been reached. "
                            "Using SQL Server data for supported questions."
                        )
                    else:
                        st.warning(
                            "Gemini is temporarily unavailable. "
                            "Using SQL Server data for supported questions."
                        )

                    answer = get_sql_fallback_answer(prompt)

                    if answer is None:
                        answer = (
                            "This question cannot currently be answered "
                            "by the SQL fallback. Gemini is unavailable, "
                            "so please try a supported question or retry later."
                        )

                    st.markdown(answer)

                else:
                    answer = (
                        "I couldn't get a response from Gemini. "
                        "Please check your API key, model availability, "
                        "usage limits, and internet connection."
                    )

                    st.error(answer)
                    st.caption(f"Technical details: {error}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )