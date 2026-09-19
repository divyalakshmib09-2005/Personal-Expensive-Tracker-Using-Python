import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px



st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)



<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

.card-title {
    font-size: 15px;
    color: #666;
}

.card-value {
    font-size: 27px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)



def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Divya@2005",
        database="expense_tracker"
    )




def get_expenses():

    conn = get_connection()

    query = """
    SELECT
        expense_id AS ID,
        expense_date AS Date,
        category AS Category,
        description AS Description,
        amount AS Amount,
        payment_method AS Payment
    FROM expenses
    ORDER BY expense_date DESC, expense_id DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df




st.sidebar.title("💰 Expense Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📋 View Expenses",
        "✏️ Update Expense",
        "🗑️ Delete Expense",
        "🔍 Search & Filter",
        "📊 Reports",
        "🎯 Budget"
    ]
)




if page == "🏠 Dashboard":

    st.markdown(
        '<div class="title">💰 Personal Expense Tracker</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track, manage and analyze your daily expenses'
        '</div>',
        unsafe_allow_html=True
    )

    df = get_expenses()

    if df.empty:

        st.warning("No expenses found.")

    else:

        total = df["Amount"].sum()
        average = df["Amount"].mean()
        count = len(df)
        highest = df["Amount"].max()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">💰 Total Expense</div>
                    <div class="card-value">₹ {total:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">📊 Average Expense</div>
                    <div class="card-value">₹ {average:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">🔢 Total Expenses</div>
                    <div class="card-value">{count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">🔥 Highest Expense</div>
                    <div class="card-value">₹ {highest:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        col1, col2 = st.columns(2)

      

        with col1:

            category_df = (
                df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                category_df,
                names="Category",
                values="Amount",
                title="📊 Category-wise Expense"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

       
        with col2:

            payment_df = (
                df.groupby("Payment")["Amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                payment_df,
                x="Payment",
                y="Amount",
                title="💳 Payment Method Summary"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("### 📋 Recent Expenses")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )




elif page == "➕ Add Expense":

    st.title("➕ Add Expense")

    with st.form("add_expense_form"):

        expense_date = st.date_input("Expense Date")

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Shopping",
                "Bills",
                "Travel",
                "Entertainment",
                "Education",
                "Health",
                "Other"
            ]
        )

        description = st.text_input(
            "Description"
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=10.0
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "UPI",
                "Card",
                "Cash"
            ]
        )

        submit = st.form_submit_button(
            "Add Expense"
        )

        if submit:

            if description.strip() == "":

                st.error("Please enter a description.")

            elif amount <= 0:

                st.error("Amount must be greater than 0.")

            else:

                conn = get_connection()

                cursor = conn.cursor()

                query = """
                INSERT INTO expenses
                (
                    expense_date,
                    category,
                    description,
                    amount,
                    payment_method
                )
                VALUES (%s, %s, %s, %s, %s)
                """

                values = (
                    expense_date,
                    category,
                    description,
                    amount,
                    payment
                )

                cursor.execute(query, values)

                conn.commit()

                cursor.close()
                conn.close()

                st.success(
                    "Expense added successfully! ✅"
                )

                st.rerun()




elif page == "📋 View Expenses":

    st.title("📋 All Expenses")

    df = get_expenses()

    if df.empty:

        st.info("No expenses found.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            "expense_report.csv",
            "text/csv"
        )




elif page == "✏️ Update Expense":

    st.title("✏️ Update Expense")

    df = get_expenses()

    if df.empty:

        st.info("No expenses available.")

    else:

        expense_id = st.number_input(
            "Enter Expense ID",
            min_value=1,
            step=1
        )

        field = st.selectbox(
            "Select field to update",
            [
                "Category",
                "Description",
                "Amount",
                "Payment Method"
            ]
        )

        new_value = st.text_input(
            "Enter new value"
        )

        if st.button("Update Expense"):

            conn = get_connection()

            cursor = conn.cursor()

            column_map = {
                "Category": "category",
                "Description": "description",
                "Amount": "amount",
                "Payment Method": "payment_method"
            }

            column = column_map[field]

            if field == "Amount":

                try:
                    new_value = float(new_value)

                except:

                    st.error(
                        "Please enter a valid amount."
                    )

                    cursor.close()
                    conn.close()

                    st.stop()

            query = f"""
            UPDATE expenses
            SET {column} = %s
            WHERE expense_id = %s
            """

            cursor.execute(
                query,
                (new_value, expense_id)
            )

            conn.commit()

            if cursor.rowcount > 0:

                st.success(
                    "Expense updated successfully! ✅"
                )

            else:

                st.error(
                    "Expense ID not found! ❌"
                )

            cursor.close()
            conn.close()




elif page == "🗑️ Delete Expense":

    st.title("🗑️ Delete Expense")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    confirm = st.checkbox(
        "I confirm that I want to delete this expense."
    )

    if st.button("Delete Expense"):

        if not confirm:

            st.warning(
                "Please confirm deletion first."
            )

        else:

            conn = get_connection()

            cursor = conn.cursor()

            query = """
            DELETE FROM expenses
            WHERE expense_id = %s
            """

            cursor.execute(
                query,
                (expense_id,)
            )

            conn.commit()

            if cursor.rowcount > 0:

                st.success(
                    "Expense deleted successfully! ✅"
                )

            else:

                st.error(
                    "Expense ID not found! ❌"
                )

            cursor.close()
            conn.close()




elif page == "🔍 Search & Filter":

    st.title("🔍 Search & Filter")

    df = get_expenses()

    if df.empty:

        st.info("No expenses found.")

    else:

        tab1, tab2, tab3 = st.tabs(
            [
                "Search by ID",
                "Search by Category",
                "Filter by Date"
            ]
        )

        
        with tab1:

            expense_id = st.number_input(
                "Enter Expense ID",
                min_value=1,
                step=1
            )

            result = df[
                df["ID"] == expense_id
            ]

            if not result.empty:

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info("Expense not found.")

     

        with tab2:

            categories = sorted(
                df["Category"].dropna().unique()
            )

            category = st.selectbox(
                "Select Category",
                categories
            )

            result = df[
                df["Category"].str.lower()
                == category.lower()
            ]

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        

        with tab3:

            start_date = st.date_input(
                "Start Date"
            )

            end_date = st.date_input(
                "End Date"
            )

            # Convert Date column to datetime
            df["Date"] = pd.to_datetime(df["Date"])

            # Convert selected dates to Timestamp
            start = pd.Timestamp(start_date)
            end = pd.Timestamp(end_date)

            # Filter expenses
            result = df[
                (df["Date"] >= start) &
                (df["Date"] <= end)
            ]

            st.dataframe(
                result,
                width="stretch",
                hide_index=True
            )



elif page == "📊 Reports":

    st.title("📊 Expense Reports")

    df = get_expenses()

    if df.empty:

        st.info("No expenses found.")

    else:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Highest Expense",
                f"₹ {df['Amount'].max():,.2f}"
            )

        with col2:

            st.metric(
                "Lowest Expense",
                f"₹ {df['Amount'].min():,.2f}"
            )

        with col3:

            st.metric(
                "Average Expense",
                f"₹ {df['Amount'].mean():,.2f}"
            )

        st.markdown("---")

        st.subheader("📊 Category-wise Spending")

        category_df = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(
                "Amount",
                ascending=False
            )
        )

        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            category_df,
            x="Category",
            y="Amount",
            title="Category-wise Spending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )




elif page == "🎯 Budget":

    st.title("🎯 Budget Management")

    budget = st.number_input(
        "Set Monthly Budget",
        min_value=0.0,
        step=500.0
    )

    df = get_expenses()

    total = df["Amount"].sum() if not df.empty else 0

    if st.button("Check Budget"):

        st.metric(
            "Monthly Budget",
            f"₹ {budget:,.2f}"
        )

        st.metric(
            "Total Expense",
            f"₹ {total:,.2f}"
        )

        if budget == 0:

            st.warning(
                "Please set a budget greater than 0."
            )

        elif total < budget:

            remaining = budget - total

            st.success(
                f"Within Budget ✅ | "
                f"Remaining: ₹ {remaining:,.2f}"
            )

        elif total == budget:

            st.warning(
                "Budget fully used ⚠️"
            )

        else:

            exceeded = total - budget

            st.error(
                f"Budget Exceeded! ❌ | "
                f"Exceeded by: ₹ {exceeded:,.2f}"
            )
