from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_print_custom_report(self):
        """Button action to trigger the PDF report"""
        return self.env.ref('ws_custom_sales_report.custom_sales_report_action').report_action(self)

