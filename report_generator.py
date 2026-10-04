import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font


def generate_report(df, summary, issues):

    report_path = "reports/AutoReport_Report.xlsx"

    # Create summary data
    summary_data = pd.DataFrame({
        "Metric": [
            "Original Records",
            "Final Records",
            "Duplicates",
            "Missing Values",
            "Total Sales",
            "Total Orders",
            "Total Quantity",
            "Average Order Value",
            "Top Product",
            "Cancelled Orders",
            "Pending Orders"
        ],

        "Value": [
            summary["original_rows"],
            summary["final_rows"],
            summary["duplicates"],
            summary["missing_values"],
            summary["total_sales"],
            summary["total_orders"],
            summary["total_quantity"],
            summary["average_order_value"],
            summary["top_product"],
            summary["cancelled_orders"],
            summary["pending_orders"]
        ]
    })

    # Create issue data
    if issues:

        issue_data = pd.DataFrame({
            "Issue": issues
        })

    else:

        issue_data = pd.DataFrame({
            "Issue": ["No issues detected"]
        })

    # Create follow-up tasks
    followups = []

    if summary["cancelled_orders"] > 0:
        followups.append([
            "HIGH",
            "Review cancelled orders",
            "Business Manager"
        ])

    if summary["pending_orders"] > 0:
        followups.append([
            "MEDIUM",
            "Follow up on pending orders",
            "Sales Team"
        ])

    if summary["duplicates"] > 0:
        followups.append([
            "MEDIUM",
            "Review duplicate records",
            "Data Team"
        ])

    if summary["missing_values"] > 0:
        followups.append([
            "LOW",
            "Review missing data",
            "Data Team"
        ])

    if not followups:
        followups.append([
            "LOW",
            "No follow-up required",
            "None"
        ])

    followup_data = pd.DataFrame(
        followups,
        columns=["Priority", "Task", "Assigned To"]
    )

    # Save Excel report
    with pd.ExcelWriter(
        report_path,
        engine="openpyxl"
    ) as writer:

        summary_data.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        issue_data.to_excel(
            writer,
            sheet_name="Issues",
            index=False
        )

        followup_data.to_excel(
            writer,
            sheet_name="Follow-up Tasks",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Cleaned Data",
            index=False
        )

    # Format workbook
    workbook = load_workbook(report_path)

    for sheet in workbook.worksheets:

        for cell in sheet[1]:
            cell.font = Font(bold=True)

        sheet.freeze_panes = "A2"

        for column in sheet.columns:

            max_length = 0

            for cell in column:

                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

            sheet.column_dimensions[
                column[0].column_letter
            ].width = min(max_length + 2, 40)

    workbook.save(report_path)

    return report_path