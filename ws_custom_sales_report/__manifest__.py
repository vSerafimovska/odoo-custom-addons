{
    "name": "Custom Sales Report",
    "summary": "This module adds a custom PDF report for sales orders",
    "license": "AGPL-3",
    "version": "0.1",
    "category": "Sales",
    "author": "",
    "website": "",
    "depends": ["sale", "web"],
    "data": [
        "report/custom_sales_report.xml",
        "views/sale_order_view.xml",

    ],
    "installable": True,
    "application": False,
}
