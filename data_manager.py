import pandas as pd
import os
import uuid

CSV_FILE = 'finance_data.csv'

def initialize_data():
    """Checks if CSV exists, creates it if not. Ensures 'Id' column exists."""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Id', 'Date', 'Amount', 'Category', 'Type', 'Description'])
        df.to_csv(CSV_FILE, index=False)
    else:
        # Check if Id column exists, if not add it
        df = pd.read_csv(CSV_FILE)
        if 'Id' not in df.columns:
            df['Id'] = [str(uuid.uuid4()) for _ in range(len(df))]
            df.to_csv(CSV_FILE, index=False)

def load_data():
    """Loads the finance data from CSV."""
    initialize_data()
    df = pd.read_csv(CSV_FILE)
    # Ensure Amount is numeric, coercing errors to NaN then filling with 0
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0.0)
    return df

def save_transaction(date, amount, category, trans_type, description):
    """Saves a new transaction to the CSV."""
    initialize_data()
    new_data = pd.DataFrame({
        'Id': [str(uuid.uuid4())],
        'Date': [date],
        'Amount': [amount],
        'Category': [category],
        'Type': [trans_type],
        'Description': [description]
    })
    new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)

def delete_transaction(transaction_id):
    """Deletes a transaction by ID."""
    df = load_data()
    df = df[df['Id'] != transaction_id]
    df.to_csv(CSV_FILE, index=False)

def update_data(df):
    """Overwrites the CSV with the provided DataFrame."""
    df.to_csv(CSV_FILE, index=False)

def get_summary():
    """Calculates total income, expenses, and savings."""
    df = load_data()
    if df.empty:
        return 0, 0, 0
    
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    savings = total_income - total_expense
    return total_income, total_expense, savings
