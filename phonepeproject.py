import streamlit as st
from streamlit_option_menu import option_menu 
import pandas as pd
import psycopg2
import plotly.express as px
import json
import requests

# SQL connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "Harini.1997",
                        database = "Phonepenew",
                        port = "5432"
                        )
cursor = mydb.cursor()

#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table7 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Insurance_type", "Insurance_count","Insurance_amount"))
#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table3 = cursor.fetchall()

Map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table5 = cursor.fetchall()

Top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))


#stream lit 

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Title
st.title("PHONEPE DATA VISUALIZATION ")



with st.sidebar:

 select= option_menu("Main Menu",["Decoding Transaction Dynamics on PhonePe", 
                                  "User Engagement and Growth Strategy",
                                  "Transaction Analysis for Market Expansion",
                                  "User Registration Analysis",
                                  "Insurance Transactions Analysis"])


# --- Home Page ---
if select == "Decoding Transaction Dynamics on PhonePe":
    st.subheader("Welcome to the PhonePe Transaction Insights Dashboard")
    

# --- Sidebar Filters ---
    st.sidebar.header("Filters")

# Filter by Year
    years = Aggre_transaction['Years'].unique()
    selected_year = st.sidebar.multiselect("Select Year(s):", years, default=years)

# Filter by Quarter
    quarters = Aggre_transaction['Quarter'].unique()
    selected_quarter = st.sidebar.multiselect("Select Quarter(s):", quarters, default=quarters)

# Filter by Transaction Type
    transaction_types = Aggre_transaction['Transaction_type'].unique()
    selected_type = st.sidebar.multiselect("Select Transaction Type(s):", transaction_types, default=transaction_types)

# Apply Filters
    df_filtered = Aggre_transaction[
      (Aggre_transaction['Years'].isin(selected_year)) &
      (Aggre_transaction['Quarter'].isin(selected_quarter)) &
      (Aggre_transaction['Transaction_type'].isin(selected_type))
      ]

    st.subheader("Filtered Data Preview")
    st.dataframe(df_filtered.head())

# --- Visualization 1: State-wise Total Transactions ---
    st.subheader("State-wise Total Transaction Amount")

    state_agg = df_filtered.groupby('States').agg({'Transaction_amount':'sum'}).reset_index()

    fig1 = px.bar(state_agg, 
              x='States', 
              y='Transaction_amount', 
              color='Transaction_amount',
              title="Total Transaction Amount by State",
              labels={'Transaction_amount':'Transaction Amount'},
              height=500)
    st.plotly_chart(fig1, use_container_width=True)

# --- Visualization 2: Quarterly Trends ---
    st.subheader("Quarterly Transaction Trends")

    quarter_agg = df_filtered.groupby(['Years', 'Quarter']).agg({'Transaction_amount':'sum'}).reset_index()
    quarter_agg['Year_Quarter'] = quarter_agg['Years'].astype(str) + '-Q' + quarter_agg['Quarter'].astype(str)

    fig2 = px.line(quarter_agg, 
               x='Year_Quarter', 
               y='Transaction_amount', 
               markers=True,
               title="Quarterly Transaction Amount Trends")
    st.plotly_chart(fig2, use_container_width=True)

# --- Visualization 3: Transaction Type Distribution ---
    st.subheader("Transaction Type Distribution")

    type_agg = df_filtered.groupby('Transaction_type').agg({'Transaction_amount':'sum'}).reset_index()

    fig3 = px.pie (type_agg, 
              values='Transaction_amount', 
              names='Transaction_type',
              title="Transaction Amount by Type")
    st.plotly_chart(fig3, use_container_width=True)

# --- Visualization 4: State vs Transaction Count (Bubble) ---
    st.subheader("State-wise Transaction Count vs Amount")

    bubble_df = df_filtered.groupby('States').agg({
    'Transaction_amount':'sum',
    'Transaction_count':'sum'
       }).reset_index()

    fig4 = px.scatter(bubble_df,
                  x='Transaction_count',
                  y='Transaction_amount',
                  size='Transaction_amount',
                  color='States',
                  title="Transaction Count vs Amount by State",
                  hover_name='States')
    st.plotly_chart(fig4, use_container_width=True)

# --- Visualization Page ---
elif select == "User Engagement and Growth Strategy":
 # Calculate engagement ratio
    Map_user['EngagementRatio'] = Map_user['AppOpens'] / Map_user['RegisteredUser']


    st.title("User Engagement and Growth Strategy - PhonePe")

# Sidebar filters
    years = st.sidebar.multiselect("Select Year(s)", sorted(Map_user['Years'].unique()), default=sorted(Map_user['Years'].unique()))
    quarters = st.sidebar.multiselect("Select Quarter(s)", sorted(Map_user['Quarter'].unique()), default=sorted(Map_user['Quarter'].unique()))
    states = st.sidebar.multiselect("Select State(s)", sorted(Map_user['States'].unique()), default=sorted(Map_user['States'].unique()))

# Apply filters
    filtered_df = Map_user[
    (Map_user['Years'].isin(years)) &
    (Map_user['Quarter'].isin(quarters)) &
    (Map_user['States'].isin(states))
 ]

    st.subheader("Overall Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registered Users", f"{filtered_df['RegisteredUser'].sum():,}")
    col2.metric("Total App Opens", f"{filtered_df['AppOpens'].sum():,}")
    overall_ratio = filtered_df['AppOpens'].sum() / filtered_df['RegisteredUser'].sum() if filtered_df['RegisteredUser'].sum() > 0 else 0
    col3.metric("Overall Engagement Ratio", f"{overall_ratio:.2f}")

# ===================== State Level Analysis =====================
    st.header("State-level Engagement Analysis")

# Aggregate at state level
    state_group = filtered_df.groupby("States").agg({
    "RegisteredUser": "sum",
    "AppOpens": "sum"
}).reset_index()
    state_group['EngagementRatio'] = state_group['AppOpens'] / state_group['RegisteredUser']

# Bar chart for Engagement Ratio
    fig_state = px.bar(
    state_group.sort_values('EngagementRatio', ascending=False),
    x="States", y="EngagementRatio",
    hover_data=["RegisteredUser", "AppOpens"],
    title="Engagement Ratio by State",
    color="EngagementRatio",
    color_continuous_scale="Blues"
)
    st.plotly_chart(fig_state, use_container_width=True)

# ===================== District Level Analysis =====================
    st.header("District-level Details")
# Show table for districts of selected states
    district_group = filtered_df.groupby(["States", "Districts"]).agg({
    "RegisteredUser": "sum",
    "AppOpens": "sum"
}).reset_index()
    district_group['EngagementRatio'] = district_group['AppOpens'] / district_group['RegisteredUser']

    st.dataframe(district_group.sort_values(['States', 'EngagementRatio'], ascending=[True, False]))

# ===================== Trends Over Time =====================
    st.header("Engagement Trend Over Time")

# Aggregate by year-quarter
    time_group = filtered_df.groupby(["Years", "Quarter"]).agg({
    "RegisteredUser": "sum",
    "AppOpens": "sum"
}).reset_index()
    time_group['EngagementRatio'] = time_group['AppOpens'] / time_group['RegisteredUser']
    time_group['Period'] = time_group['Years'].astype(str) + "-Q" + time_group['Quarter'].astype(str)

    fig_time = px.line(
    time_group,
    x="Period", y="EngagementRatio",
    markers=True,
    title="Engagement Ratio Trend Over Time"
)
    st.plotly_chart(fig_time, use_container_width=True)

    st.caption("Engagement Ratio = App Opens ÷ Registered Users")
# --- Raw Data Page ---
# --- Raw Data Page ---
elif select == "Transaction Analysis for Market Expansion":    

   Top_transaction['Avg_txn_value'] = Top_transaction['Transaction_amount'] / Top_transaction['Transaction_count']

   st.set_page_config(page_title="PhonePe Transaction Analysis", layout="wide")

   st.title("Transaction Analysis for Market Expansion - PhonePe")

# Sidebar filters
   years = st.sidebar.multiselect("Select Year(s)", sorted(Top_transaction['Years'].unique()),
                                default=sorted(Top_transaction['Years'].unique()) ,key="state_multiselect_top_years")
   quarters = st.sidebar.multiselect("Select Quarter(s)", sorted(Top_transaction['Quarter'].unique()),
                                   default=sorted(Top_transaction['Quarter'].unique()) ,key="state_multiselect_top_Quarters")

# Apply filters
   filtered_df = Top_transaction[
    (Top_transaction['Years'].isin(years)) &
    (Top_transaction['Quarter'].isin(quarters))
    ]

# Overall Metrics
   st.subheader("Overall Metrics")
   col1, col2, col3 = st.columns(3)
   total_txns = filtered_df['Transaction_count'].sum()
   total_amount = filtered_df['Transaction_amount'].sum()
   avg_value = total_amount / total_txns if total_txns > 0 else 0
   col1.metric("Total Transactions", f"{total_txns:,}")
   col2.metric("Total Transaction Amount", f"₹{total_amount:,.0f}")
   col3.metric("Average Transaction Value", f"₹{avg_value:,.2f}")

# ================== State-level Aggregation ==================
   state_group = filtered_df.groupby("States").agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum"
    }).reset_index()
   state_group['Avg_txn_value'] = state_group['Transaction_amount'] / state_group['Transaction_count']

# Bar chart: Total transaction amount by state
   st.header("State-wise Transaction Amount")
   fig_bar = px.bar(
    state_group.sort_values('Transaction_amount', ascending=False),
    x="States", y="Transaction_amount",
    hover_data=["Transaction_count", "Avg_txn_value"],
    title="Total Transaction Amount by State",
    color="Transaction_amount",
    color_continuous_scale="Purples"
   )
   st.plotly_chart(fig_bar, use_container_width=True)

# Scatter Plot: Count vs Amount
   st.header("Transaction Dynamics (Volume vs. Value)")
   fig_scatter = px.scatter(
    state_group,
    x="Transaction_count",
    y="Transaction_amount",
    size="Avg_txn_value",
    color="States",
    hover_data=["Avg_txn_value"],
    title="Transaction Count vs Transaction Amount by State"
   )
   st.plotly_chart(fig_scatter, use_container_width=True)

# ================== Trends Over Time ==================
   st.header("Transaction Trends Over Time")

# Aggregate by year and quarter
   time_group = filtered_df.groupby(["Years", "Quarter"]).agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum"
   }).reset_index()
   time_group['Avg_txn_value'] = time_group['Transaction_amount'] / time_group['Transaction_count']
   time_group['Period'] = time_group['Years'].astype(str) + "-Q" + time_group['Quarter'].astype(str)

   fig_trend = px.line(
    time_group,
    x="Period",
    y=["Transaction_count", "Transaction_amount"],
    markers=True,
    title="Transaction Count and Amount Trend Over Time"
   )
   st.plotly_chart(fig_trend, use_container_width=True)

   st.caption("Avg Transaction Value = Transaction Amount ÷ Transaction Count")


elif select == "User Registration Analysis": 


  st.title("User Registration Analysis - PhonePe")

# Sidebar filters
  years = st.sidebar.multiselect(
    "Select Year(s)", 
    sorted(Aggre_user['Years'].unique()), 
    default=sorted(Aggre_user['Years'].unique()),key="state_multiselect_top_Years_1"
    )

  quarters = st.sidebar.multiselect(
    "Select Quarter(s)", 
    sorted(Aggre_user['Quarter'].unique()), 
    default=sorted(Aggre_user['Quarter'].unique()),key="state_multiselect_top_Quarters_1"
   )

# Apply filters
  filtered_df = Aggre_user[
    (Aggre_user['Years'].isin(years)) &
    (Aggre_user['Quarter'].isin(quarters))
]

# ===================== Overall Metrics =====================
  st.subheader("Overall Metrics")
  col1, col2 = st.columns(2)
  total_registrations = filtered_df['Transaction_count'].sum()
  col1.metric("Total Registrations", f"{total_registrations:,}")
  col2.metric("Unique States", f"{filtered_df['States'].nunique()}")

# ===================== Top States =====================
  st.header("Top States by User Registrations")

  state_group = filtered_df.groupby("States").agg({
    "Transaction_count": "sum"
  }).reset_index()

  fig_states = px.bar(
    state_group.sort_values("Transaction_count", ascending=False),
    x="States", y="Transaction_count",
    title="User Registrations by State",
    color="Transaction_count",
    color_continuous_scale="Blues"
  )
  st.plotly_chart(fig_states, use_container_width=True)

# ===================== Brand/Device Insights =====================
  st.header("Registrations by Device Brand")

  brand_group = filtered_df.groupby("Brands").agg({
    "Transaction_count": "sum",
    "Percentage": "mean"
  }).reset_index()

  fig_brands = px.pie(
    brand_group,
    names="Brands",
    values="Transaction_count",
    title="Registrations Distribution by Device Brand"
  )
  st.plotly_chart(fig_brands, use_container_width=True)

# ===================== Trend Over Time =====================
  st.header("Registration Trends Over Time")

# Aggregate registrations by time
  time_group = filtered_df.groupby(["Years", "Quarter"]).agg({
    "Transaction_count": "sum"
  }).reset_index()
  time_group['Period'] = time_group['Years'].astype(str) + "-Q" + time_group['Quarter'].astype(str)

  fig_trend = px.line(
    time_group,
    x="Period", y="Transaction_count",
    markers=True,
    title="User Registration Trends Over Time"
  )
  st.plotly_chart(fig_trend, use_container_width=True)

  st.caption("This dashboard highlights top states and device brands contributing to PhonePe user registrations.")

elif select == "Insurance Transactions Analysis": 
   
  st.title("Insurance Transactions Analysis - PhonePe")

# Sidebar filters
  years = st.sidebar.multiselect(
    "Select Year(s)",
    sorted(Map_insurance['Years'].unique()),
    default=sorted(Map_insurance['Years'].unique())
    )

  quarters = st.sidebar.multiselect(
    "Select Quarter(s)",
    sorted(Map_insurance['Quarter'].unique()),
    default=sorted(Map_insurance['Quarter'].unique())
    )

# Apply filters
  filtered_df = Map_insurance[
    (Map_insurance['Years'].isin(years)) &
    (Map_insurance['Quarter'].isin(quarters))
 ]

# ===================== Overall Metrics =====================
  st.subheader("Overall Metrics")
  col1, col2, col3 = st.columns(3)
  total_txns = filtered_df['Transaction_count'].sum()
  total_amount = filtered_df['Transaction_amount'].sum()
  avg_value = total_amount / total_txns if total_txns > 0 else 0
  col1.metric("Total Insurance Transactions", f"{total_txns:,}")
  col2.metric("Total Transaction Amount", f"₹{total_amount:,.0f}")
  col3.metric("Avg Transaction Value", f"₹{avg_value:,.2f}")

# ===================== State Level =====================
  st.header("Top States by Insurance Transactions")

  state_group = filtered_df.groupby("States").agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum"
  }).reset_index()

  fig_state = px.bar(
    state_group.sort_values("Transaction_count", ascending=False),
    x="States", y="Transaction_count",
    hover_data=["Transaction_amount"],
    title="Insurance Transactions by State",
    color="Transaction_count",
    color_continuous_scale="Blues"
  )
  st.plotly_chart(fig_state, use_container_width=True)

# ===================== District Level =====================
  st.header("District-Level Insurance Transactions")

  district_group = filtered_df.groupby(["States", "Districts"]).agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum"
  }).reset_index()

  st.dataframe(
    district_group.sort_values(
        ["States", "Transaction_count"], ascending=[True, False]
    ),
    use_container_width=True
  )

# ===================== Trend Over Time =====================
  st.header("Insurance Transaction Trends Over Time")

  time_group = filtered_df.groupby(["Years", "Quarter"]).agg({
    "Transaction_count": "sum",
    "Transaction_amount": "sum"
  }).reset_index()
  time_group["Period"] = time_group["Years"].astype(str) + "-Q" + time_group["Quarter"].astype(str)

  fig_trend = px.line(
    time_group,
    x="Period", y="Transaction_count",
    markers=True,
    title="Insurance Transactions Over Time"
  )
  st.plotly_chart(fig_trend, use_container_width=True)

  st.caption("This dashboard helps analyze insurance transactions across states and districts.")
