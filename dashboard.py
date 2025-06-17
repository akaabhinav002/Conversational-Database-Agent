
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_connection import db

def show_dashboard():
    st.markdown("## 🌐DataBase Insights Dashboard")

    # --- Basic stats ---
    total_customers = db["customers"].count_documents({})
    total_accounts = db["accounts"].count_documents({})
    total_transactions = db["transactions"].count_documents({})

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Customers", total_customers)
    col2.metric("💼 Accounts", total_accounts)
    col3.metric("📦 Transaction Buckets", total_transactions)

    st.markdown("---")

    # --- Tier distribution ---
    st.markdown("### 🏷️ Customer Tier Distribution")
    pipeline = [
        {"$project": {"tiers": {"$objectToArray": "$tier_and_details"}}},
        {"$unwind": "$tiers"},
        {"$group": {"_id": "$tiers.v.tier", "count": {"$sum": 1}}},
    ]
    tier_data = list(db["customers"].aggregate(pipeline))

    if tier_data:
        df = pd.DataFrame(tier_data)
        fig, ax = plt.subplots()
        ax.bar(df["_id"], df["count"], color="skyblue")
        ax.set_xlabel("Tier")
        ax.set_ylabel("Customer Count")
        st.pyplot(fig)

    st.markdown("---")

   
    st.markdown("### 🧾 Account Products Distribution")
    product_pipeline = [
        {"$unwind": "$products"},
        {"$group": {"_id": "$products", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    product_data = list(db["accounts"].aggregate(product_pipeline))
    if product_data:
        prod_df = pd.DataFrame(product_data).set_index("_id")
        st.bar_chart(prod_df)

    st.markdown("---")

    
    st.markdown("### 🕓 Latest Transaction Buckets")
    recent_txns = db["transactions"].find().sort("bucket_end_date", -1).limit(5)
    for txn in recent_txns:
        st.markdown(f"- **Account:** `{txn['account_id']}` | Transactions: `{txn['transaction_count']}`")
