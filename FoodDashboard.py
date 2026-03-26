import streamlit as st
import pandas as pd

st.title("Food Dashboard")

uploaded_file = st.file_uploader("Upload your food dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Data Preview:")
    st.dataframe(df)

    # ------------------ FILTERS ------------------
    st.sidebar.header("🔍 Filters")

    # City Filter
    if 'City' in df.columns:
        city = st.sidebar.selectbox("Select City", ["All"] + list(df['City'].unique()))
    else:
        city = "All"

    # Order Type Filter
    if 'Order_Type' in df.columns:
        order_type = st.sidebar.selectbox("Order Type", ["All"] + list(df['Order_Type'].unique()))
    else:
        order_type = "All"

    # Amount Filter
    if 'Amount' in df.columns:
        min_amount = int(df['Amount'].min())
        max_amount = int(df['Amount'].max())

        amount_range = st.sidebar.slider(
            "Select Amount Range",
            min_amount,
            max_amount,
            (min_amount, max_amount)
        )
    else:
        amount_range = None

    # ------------------ APPLY FILTERS ------------------
    filtered_df = df.copy()

    if city != "All":
        filtered_df = filtered_df[filtered_df['City'] == city]

    if order_type != "All":
        filtered_df = filtered_df[filtered_df['Order_Type'] == order_type]

    if amount_range:
        filtered_df = filtered_df[
            (filtered_df['Amount'] >= amount_range[0]) &
            (filtered_df['Amount'] <= amount_range[1])
        ]

    # ------------------ KPIs ------------------
    st.header("📊 Key Performance Indicators")

    total_orders = filtered_df.shape[0]
    total_revenue = filtered_df['Amount'].sum()
    avg_rating = filtered_df['Rating'].mean()
    avg_delivery_time = filtered_df['Delivery_Time'].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_orders)
    col2.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col3.metric("Avg Rating", round(avg_rating, 2))
    col4.metric("Avg Delivery Time", f"{round(avg_delivery_time, 2)} mins")

    # ------------------ TABS ------------------
    tab1, tab2, tab3 = st.tabs(["Data", " Charts", "AI Recommendations"])

    # TAB 1
    with tab1:
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

    # TAB 2
    with tab2:
        st.subheader("Insights")

        if 'City' in filtered_df.columns:
            st.write("Revenue by City")
            city_revenue = filtered_df.groupby('City')['Amount'].sum()
            st.bar_chart(city_revenue)

        if 'Food' in filtered_df.columns:
            st.write("Orders by Food")
            food_orders = filtered_df['Food'].value_counts()
            st.bar_chart(food_orders)

    # TAB 3
    with tab3:
        st.subheader("Smart Recommendations")

        if avg_rating < 3.5:
            st.warning("Improve food quality or service")

        if avg_delivery_time > 30:
            st.error("Delivery time too high")

        if total_revenue < 1000:
            st.info("Revenue is low. Consider discounts or ads")

        st.success("Dashboard analysis complete!")

else:
    st.warning("Please upload a CSV file")