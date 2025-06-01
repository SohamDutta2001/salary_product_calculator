import streamlit as st
import webbrowser

st.set_page_config(page_title="Work-Time Product Cost Calculator", page_icon="💰")

st.title("💰 Work-Time Product Cost Calculator")

st.header("🧾 Basic Financial Inputs")

# --- Mandatory Field Warning Flag ---
missing_input = False

# Monthly income (mandatory)
inc_monthly = st.number_input("Monthly income*", min_value=0.0, format="%.2f", key="inc_monthly")
if inc_monthly == 0.0:
    missing_input = True

# Work hours per day (mandatory)
hrs_work = st.number_input("Hours of work per day*", min_value=1.0, max_value=24.0, format="%.1f", key="hrs_work")
if hrs_work == 0.0:
    missing_input = True

# Office type
type_ofc = st.selectbox("Office Type*", options=["", "WFH", "WFO"], key="type_ofc")
if type_ofc == "":
    missing_input = True

# Commute Details (if WFO)
n_days_wfo, hour_daily_commute, minute_daily_commute, amt_daily_commute = 0, 0, 0, 0.0
if type_ofc == "WFO":
    n_days_wfo = st.number_input("No. of days WFO*", min_value=0, max_value=7, key="n_days_wfo")
    hour_daily_commute = st.slider("Daily commute hours", 0, 7, 0, key="commute_hour")
    minute_daily_commute = st.slider("Daily commute minutes", 0, 59, 0, key="commute_minute")
    amt_daily_commute = st.number_input("Daily commute expense", min_value=0.0, step=10.0, key="amt_daily_commute")
    commute_time_total = hour_daily_commute + (minute_daily_commute / 60.0)
else:
    commute_time_total = 0

# Home Type
type_home = st.selectbox("Home*", options=["", "Home", "Rented apartment or PG"], key="type_home")
if type_home == "":
    missing_input = True

# Rent (if rented)
amt_rent = 0.0
if type_home == "Rented apartment or PG":
    amt_rent = st.number_input("rent", min_value=0.0, step=100.0, key="amt_rent")

# EMI 
amt_emi_monthly = st.number_input("recurring emi (optional)", min_value=0.0, step=500.0, key="amt_emi_monthly")
if amt_emi_monthly == 0.0:
    missing_input = False

# Savings (optional)
amt_savings_monthly = st.number_input("Savings (optional)", min_value=0.0, step=500.0, key="amt_savings_monthly")

# --- Net Salary Calculation ---
monthly_office_expense = n_days_wfo * amt_daily_commute if type_ofc == "WFO" else 0
total_deductions = amt_rent + amt_emi_monthly + amt_savings_monthly + monthly_office_expense
net_monthly_income = inc_monthly - total_deductions

if missing_input:
    st.warning("⚠️ Please fill in all mandatory fields marked with * above to proceed.")
elif net_monthly_income <= 0:
    st.error("💸 Your net income is zero or negative after deductions. Maybe rob a bank? (Just kidding, please revise your inputs!)")
else:
    daily_income = net_monthly_income / 30
    effective_work_hours = hrs_work + commute_time_total
    hourly_income = daily_income / effective_work_hours

    st.markdown("### 💼 Your Effective Earnings")
    st.write(f"**Net Monthly Income:** ₹{net_monthly_income:,.2f}")
    st.write(f"**Daily Income:** ₹{daily_income:,.2f}")
    st.write(f"**Hourly Income (incl. commute):** ₹{hourly_income:,.2f}")

    # --- Product Section ---
    st.markdown("---")
    st.header("🎯 Product Purchase Calculator")

    product_name = st.text_input("Product Name")
    product_cost = st.number_input("Product Cost (₹)", min_value=0.0, step=100.0)

    if product_name.strip() and product_cost > 0:
        total_hours = product_cost / hourly_income
        total_days = total_hours / effective_work_hours
        st.success(f"To buy **{product_name}**, you need to work for:")
        st.write(f"➡️ **{total_hours:.2f} hours** (≈ {total_days:.2f} working days)")

    # --- Footer Funny Message ---
    st.markdown("---")
    st.markdown(
        "<div style='color:gray; font-size:14px;'>"
        "💡 Remember: If a product feels too expensive in hours, don't drop your dreams... "
        "<b>just drop your job and find a better paying one 😄💼</b>"
        "</div>",
        unsafe_allow_html=True
    )

    # --- LinkedIn Button ---
    if st.button("🚀 Visit LinkedIn"):
        webbrowser.open_new_tab("https://www.linkedin.com")

st.markdown("---")
st.caption("Built with ❤️ by Sinjini & Soham")
