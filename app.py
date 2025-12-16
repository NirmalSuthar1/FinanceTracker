import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import data_manager as dm

# Page Configuration
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal Finance Tracker")

# Sidebar - Add Transaction
st.sidebar.header("Add New Transaction")
with st.sidebar.form("transaction_form", clear_on_submit=True):
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Rent", "Transport", "Entertainment", "Salary", "Freelance", "Other"])
    trans_type = st.radio("Type", ["Expense", "Income"])
    description = st.text_input("Description")
    
    submitted = st.form_submit_button("Add Transaction")
    if submitted:
        if amount > 0:
            dm.save_transaction(date, amount, category, trans_type, description)
            st.sidebar.success("Transaction Added!")
        else:
            st.sidebar.error("Amount must be greater than 0")

# Main Dashboard
# Load Data
df = dm.load_data()

# Metrics
total_income, total_expense, savings = dm.get_summary()

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"₹{total_income:,.2f}")
col2.metric("Total Expenses", f"₹{total_expense:,.2f}")
col3.metric("Current Savings", f"₹{savings:,.2f}", delta_color="normal")

st.markdown("---")

# Visualizations
if not df.empty:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Expenses by Category")
        expenses = df[df['Type'] == 'Expense']
        if not expenses.empty:
            fig1, ax1 = plt.subplots()
            expenses.groupby('Category')['Amount'].sum().plot.pie(autopct='%1.1f%%', ax=ax1)
            ax1.set_ylabel('')
            st.pyplot(fig1)
        else:
            st.info("No expenses recorded yet.")

    with col_chart2:
        st.subheader("Income vs Expenses")
        # Simple bar chart
        fig2, ax2 = plt.subplots()
        summary_df = pd.DataFrame({
            'Type': ['Income', 'Expense'],
            'Amount': [total_income, total_expense]
        })
        ax2.bar(summary_df['Type'], summary_df['Amount'], color=['green', 'red'])
        st.pyplot(fig2)

    # Recent Transactions
    st.subheader("Recent Transactions")
    
    # Use data_editor to allow deletion
    edited_df = st.data_editor(
        df.sort_values(by="Date", ascending=False),
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor",
        hide_index=True,
        column_config={
            "Id": None  # Hide the Id column
        }
    )

    # Check if data has changed (rows deleted)
    if len(edited_df) != len(df):
        dm.update_data(edited_df)
        st.rerun()

else:
    st.info("No transactions found. Add one from the sidebar to get started!")
