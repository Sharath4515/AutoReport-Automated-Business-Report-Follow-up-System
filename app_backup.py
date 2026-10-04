import streamlit as st
import matplotlib.pyplot as plt

from automation import process_data
from report_generator import generate_report


# Page configuration
st.set_page_config(
    page_title="AutoReport",
    page_icon="📊",
    layout="wide"
)


# Title
st.title("📊 AutoReport")

st.subheader(
    "Automated Business Report & Follow-up System"
)

st.write(
    "Upload your business data and AutoReport will "
    "automatically clean, analyze, detect issues, "
    "generate reports and create follow-up tasks."
)


# File upload
uploaded_file = st.file_uploader(
    "📁 Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)


# Run automation
if uploaded_file is not None:

    st.success("File uploaded successfully!")

    if st.button("🚀 Run Automation"):

        # Process data
        with st.spinner("Processing your data..."):

            df, summary, issues = process_data(
                uploaded_file
            )

        st.success("✅ Automation completed successfully!")

        # Generate report
        report_path = generate_report(
            df,
            summary,
            issues
        )

        st.success("📄 Report generated successfully!")

        # Download report
        with open(report_path, "rb") as file:

            st.download_button(
                label="📥 Download Excel Report",
                data=file,
                file_name="AutoReport_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


        # --------------------------------
        # BUSINESS SUMMARY
        # --------------------------------

        st.divider()

        st.subheader("📊 Business Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Sales",
            f"₹{summary['total_sales']:,.0f}"
        )

        col2.metric(
            "Total Orders",
            summary["total_orders"]
        )

        col3.metric(
            "Average Order Value",
            f"₹{summary['average_order_value']:,.0f}"
        )

        col4.metric(
            "Top Product",
            summary["top_product"]
        )


        # --------------------------------
        # DATA QUALITY
        # --------------------------------

        st.divider()

        st.subheader("🔍 Data Quality")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Original Records",
            summary["original_rows"]
        )

        col2.metric(
            "Duplicates",
            summary["duplicates"]
        )

        col3.metric(
            "Missing Values",
            summary["missing_values"]
        )


        # --------------------------------
        # ISSUES
        # --------------------------------

        st.divider()

        st.subheader("⚠️ Issues Detected")

        if issues:

            for issue in issues:
                st.warning(issue)

        else:

            st.success("✅ No issues detected!")


        # --------------------------------
        # BUSINESS ANALYTICS
        # --------------------------------

        st.divider()

        st.subheader("📈 Business Analytics")


        # Sales by Product
        st.write("### 💰 Sales by Product")

        sales_by_product = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig1, ax1 = plt.subplots()

        sales_by_product.plot(
            kind="bar",
            ax=ax1
        )

        ax1.set_xlabel("Product")
        ax1.set_ylabel("Sales")
        ax1.set_title("Sales by Product")

        plt.xticks(rotation=45)

        st.pyplot(fig1)

        plt.close(fig1)


        # Order Status
        st.write("### 📦 Order Status")

        status_counts = df["Status"].value_counts()

        fig2, ax2 = plt.subplots()

        status_counts.plot(
            kind="bar",
            ax=ax2
        )

        ax2.set_xlabel("Status")
        ax2.set_ylabel("Number of Orders")
        ax2.set_title("Order Status Distribution")

        plt.xticks(rotation=0)

        st.pyplot(fig2)

        plt.close(fig2)


        # --------------------------------
        # FOLLOW-UP TASKS
        # --------------------------------

        st.divider()

        st.subheader("✅ Follow-up Tasks")


        if summary["cancelled_orders"] > 0:

            st.error(
                "🔴 HIGH — Review cancelled orders"
            )


        if summary["pending_orders"] > 0:

            st.warning(
                "🟠 MEDIUM — Follow up on pending orders"
            )


        if summary["duplicates"] > 0:

            st.warning(
                "🟡 MEDIUM — Review duplicate records"
            )


        if summary["missing_values"] > 0:

            st.info(
                "🔵 LOW — Review missing data"
            )


        if (
            summary["cancelled_orders"] == 0
            and summary["pending_orders"] == 0
            and summary["duplicates"] == 0
            and summary["missing_values"] == 0
        ):

            st.success(
                "🎉 No follow-up tasks required!"
            )


        # --------------------------------
        # PROCESSED DATA
        # --------------------------------

        st.divider()

        st.subheader("📋 Processed Data")

        st.dataframe(
            df,
            use_container_width=True
        )