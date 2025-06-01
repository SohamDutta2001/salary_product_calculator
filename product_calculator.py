import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page
st.set_page_config(page_title="Work-To-Buy Calculator 💰", layout="centered")
st.title("🧮 Work-To-Buy: Reality Check Calculator")

# Exchange rates (as of now — can be updated manually)
currency_rates = {
    "INR": 1,
    "USD": 83.5,
    "EUR": 90.1,
    "GBP": 105.6,
    "ILS": 22.5  # Israeli Shekel
}

# Section: Basic Info
st.header("💼 Salary Details")
currency = st.selectbox("Select Your Currency *", list(currency_rates.keys()))
inc_monthly = st.number_input("Monthly Salary *", min_value=0.0, format="%.2f")
work_hrs = st.number_input("Company Working Hours Per Day *", min_value=1, max_value=12, value=8)

# Section: Living Situation
st.header("🏠 Living Situation")
house_owned = st.radio("Do you live in your own home? *", ["Yes", "No"])
amt_rent = 0
if house_owned == "No":
    amt_rent = st.number_input("Monthly Rent Amount", min_value=0.0, format="%.2f")

# Section: WFH/WFO
st.header("💼 Work From Office Details")
wfo_status = st.radio("Do you go to office (WFO)? *", ["Yes", "No"])
wfo_days = 0
daily_commute_expense = 0
commute_time_total = 0

if wfo_status == "Yes":
    wfo_days = st.slider("How many days a week do you go to office? *", 1, 7, 5)
    daily_commute_expense = st.number_input("Daily Commute Expense", min_value=0.0, format="%.2f")
    
    st.markdown("### 🚗 Commute Time Per Day")
    commute_hours = st.slider("Hours", 0, 5, 1)
    commute_minutes = st.slider("Minutes", 0, 59, 30)
    commute_time_total = commute_hours + commute_minutes / 60

# Section: EMI + Savings
st.header("📉 Monthly Obligations")
amt_emi_monthly = st.number_input("Monthly EMI (if any)", min_value=0.0, format="%.2f")
amt_savings_monthly = st.number_input("Desired Monthly Saving", min_value=0.0, format="%.2f")

# Section: Product Info
st.header("🎯 Product Goal")
product_name = st.text_input("Product Name (e.g. iPhone 15 Pro)")
product_cost_local = st.number_input("Product Cost in selected currency", min_value=0.0, format="%.2f")

# --- Calculations ---
monthly_office_expense = wfo_days * 4 * daily_commute_expense  # 4 weeks
monthly_commute_hours = wfo_days * 4 * commute_time_total

# Total deductions
total_deductions = amt_rent + amt_emi_monthly + amt_savings_monthly + monthly_office_expense
net_monthly_income = inc_monthly - total_deductions
daily_income = net_monthly_income / 30
effective_work_hours = work_hrs + (commute_time_total if wfo_status == "Yes" else 0)
hourly_income = daily_income / effective_work_hours if effective_work_hours > 0 else 0

# Convert product cost to INR
product_cost_inr = product_cost_local * currency_rates[currency]

# Calculate hours to afford product
hours_to_work = product_cost_inr / hourly_income if hourly_income > 0 else 0
days_to_work = hours_to_work / 24
# Section: Results
# Add this dictionary before results section
currency_symbols = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "ILS": "₪"
}

symbol = currency_symbols[currency]  # Get selected symbol

# Validation
missing_input = (
    currency == "" or
    inc_monthly == 0 or
    work_hrs == 0 or
    (house_owned == "No" and amt_rent == 0) or
    (wfo_status == "Yes" and (wfo_days == 0 or daily_commute_expense == 0)) or
    product_name.strip() == "" or
    product_cost_local == 0
)

if missing_input:
    st.warning("⚠️ Please fill in all mandatory fields marked with * above to proceed.")
elif net_monthly_income <= 0:
    st.error("💸 Your net income is zero or negative after deductions. Maybe rob a bank? (Just kidding, please revise your inputs!)")
else:
    # Proceed to show results and visualizations
    st.header("📊 Results")
    col1, col2 = st.columns(2)
    symbol = currency_symbols[currency]
    col1.metric("Net Monthly Income", f"{symbol}{net_monthly_income:,.2f}")
    col2.metric("Hourly Income", f"{symbol}{hourly_income:.2f}")
    
    st.markdown(f"To buy a **{product_name}**, you need to work for approximately **{hours_to_work:.1f} hours** (**{days_to_work:.1f} days**) straight!")
    
# --- Visualizations ---
st.header("🧩 Simulations")

# 1. Income breakdown pie chart
labels = ["Rent", "EMI", "Savings", "Commute", "Remaining"]
values = [amt_rent, amt_emi_monthly, amt_savings_monthly, monthly_office_expense, net_monthly_income]
fig1 = px.pie(names=labels, values=values, title="💸 Monthly Income Distribution")
st.plotly_chart(fig1, use_container_width=True)

# 💡 Fun note at the end
st.markdown("---")
st.markdown("### 🧠 Final Thought")
st.info("If you think your salary can't afford your dreams, don't drop the dream — just drop the job. 😄")

# Redirect to LinkedIn
if st.button("🚀 Go to LinkedIn"):
    st.markdown("[Click here to open LinkedIn](https://www.linkedin.com)", unsafe_allow_html=True)

st.markdown("---")
st.caption("Built with ❤️ by Sinjini & Soham")
