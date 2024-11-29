{
    "name": "Sale Order Email Notification",
    "summary": "Send an email when a sale order is confirmed",
    "license": "AGPL-3",
    "version": "0.1",
    "category": "Sales",
    "author": "",
    "website": "",
    "depends": ["base", "sale", "mail"],
    "data": [
        "views/email_template.xml",
        "data/email_template_data.xml",
    ],
    "installable": True,
    "auto_install": False,
}
