
import pandas as pd


def process_data(file):

    # Read file
    if isinstance(file, str):

        if file.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

    else:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

    original_rows = len(df)

    # Remove duplicate records
    duplicate_count = df.duplicated().sum()
    df = df.drop_duplicates()

    # Handle missing values
    missing_count = df.isnull().sum().sum()
    df = df.dropna()

    # Calculate sales
    df["Sales"] = df["Quantity"] * df["Unit_Price"]

    # Calculate KPIs
    total_sales = df["Sales"].sum()
    total_orders = len(df)
    total_quantity = df["Quantity"].sum()

    if total_orders > 0:
        average_order_value = total_sales / total_orders
    else:
        average_order_value = 0

    # Find top product
    product_sales = df.groupby("Product")["Sales"].sum()

    if len(product_sales) > 0:
        top_product = product_sales.idxmax()
    else:
        top_product = "N/A"

    # Detect issues
    issues = []

    if duplicate_count > 0:
        issues.append(
            f"{duplicate_count} duplicate records were found."
        )

    if missing_count > 0:
        issues.append(
            f"{missing_count} missing values were found."
        )

    cancelled_orders = len(
        df[df["Status"].str.lower() == "cancelled"]
    )

    if cancelled_orders > 0:
        issues.append(
            f"{cancelled_orders} cancelled orders require review."
        )

    pending_orders = len(
        df[df["Status"].str.lower() == "pending"]
    )

    if pending_orders > 0:
        issues.append(
            f"{pending_orders} pending orders require follow-up."
        )

    # Summary
    summary = {
        "original_rows": original_rows,
        "final_rows": len(df),
        "duplicates": duplicate_count,
        "missing_values": missing_count,
        "total_sales": total_sales,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "average_order_value": average_order_value,
        "top_product": top_product,
        "cancelled_orders": cancelled_orders,
        "pending_orders": pending_orders
    }
    # Generate automated business insights
    insights = []

    if total_sales > 200000:
        insights.append(
            "Strong sales performance: total sales exceeded ₹2 lakh."
        )
    else:
        insights.append(
            "Sales are below ₹2 lakh and may need improvement."
        )

    if top_product != "N/A":
        insights.append(
            f"{top_product} is the top-performing product by sales."
        )

    if cancelled_orders > 0:
        insights.append(
            f"{cancelled_orders} cancelled order(s) require review."
        )

    if pending_orders > 0:
        insights.append(
            f"{pending_orders} pending order(s) require follow-up."
        )
    return df, summary, issues, insights


# Test the automation
# Test the automation
if __name__ == "__main__":

    df, summary, issues, insights = process_data(
        "data/input/sales_data.csv"
    )

    print("\nSUMMARY")
    print(summary)

    print("\nISSUES")

    for issue in issues:
        print("-", issue)

    print("\nINSIGHTS")

    for insight in insights:
        print("-", insight)
