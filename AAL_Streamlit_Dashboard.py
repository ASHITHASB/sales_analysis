
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
st.title("🧭 AAL Q4 2020 Sales Dashboard")

uploaded_file = st.file_uploader("Upload AusApparalSales4thQrt2020.csv", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Month'] = data['Date'].dt.month
    data['Week'] = data['Date'].dt.isocalendar().week
    data['Quarter'] = data['Date'].dt.quarter
    data['Hour'] = data['Date'].dt.hour

    st.success("Data loaded successfully!")

    # State filter
    st.sidebar.header("🔍 Filter by State")
    state = st.sidebar.selectbox("Select State", options=data['State'].unique())
    filtered_state = data[data['State'] == state]

    st.subheader(f"📊 Sales by Demographic in {state}")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_state, x='Demographic_Group', y='Sales', ax=ax1)
    st.pyplot(fig1)

    # Demographic filter
    st.sidebar.header("👨‍👩‍👧 Filter by Demographic Group")
    group = st.sidebar.selectbox("Select Group", options=data['Demographic_Group'].unique())
    filtered_group = data[data['Demographic_Group'] == group]

    st.subheader(f"📈 Sales Trend for {group}")
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=filtered_group, x='Date', y='Sales', hue='State', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Time-of-day histogram
    st.subheader("🕒 Sales by Hour of Day")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.histplot(data['Hour'], bins=24, kde=True, ax=ax3)
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("Sales Frequency")
    st.pyplot(fig3)

    # Box plot for descriptive analysis
    st.subheader("📦 Sales Distribution by Group")
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='Demographic_Group', y='Sales', data=data, ax=ax4)
    st.pyplot(fig4)

    # Summary
    st.markdown("### 📌 Insights")
    top_states = data.groupby('State')['Sales'].sum().sort_values(ascending=False)
    top_group = data.groupby('Demographic_Group')['Sales'].sum().sort_values(ascending=False)
    st.write("Top States by Total Sales:")
    st.dataframe(top_states)
    st.write("Top Groups by Total Sales:")
    st.dataframe(top_group)
else:
    st.info("Please upload the CSV file to begin.")
