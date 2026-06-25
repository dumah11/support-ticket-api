import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Support Ticket Dashboard",
    layout="wide"
)

st.title("Support Ticket Dashboard")

conn = sqlite3.connect("tickets.db")

df = pd.read_sql_query(
    "SELECT * FROM tickets",
    conn
)

conn.close()

if df.empty:
    st.warning("No tickets found. Create tickets using the FastAPI /docs page first.")
else:
    col1, col2, col3 = st.columns(3)

    total_tickets = len(df)
    open_tickets = len(df[df["status"] == "Open"])
    closed_tickets = len(df[df["status"] == "Closed"])

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("Closed Tickets", closed_tickets)

    st.subheader("Tickets By Priority")
    st.bar_chart(df["priority"].value_counts())

    st.subheader("Tickets By Category")
    st.bar_chart(df["category"].value_counts())

    st.subheader("Tickets By Assigned Agent")

    assigned_df = df[df["assigned_to"] != ""]

    if len(assigned_df) > 0:
        st.bar_chart(assigned_df["assigned_to"].value_counts())
    else:
        st.write("No tickets assigned yet.")

    st.subheader("All Tickets")
    st.dataframe(df, use_container_width=True)