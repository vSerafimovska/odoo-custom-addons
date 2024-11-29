from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_applied = fields.Float(string='Discount Applied', compute='_compute_discount', store=True)

    @api.depends('amount_total', 'partner_id')
    def _compute_discount(self):
        for order in self:
            discount = 0.0


            if order.amount_total >= 500:
                discount = 15.0
            elif order.amount_total >= 300:
                discount = 10.0


            if order.partner_id.name == 'Mitchell Admin':
                discount = 5.0


            order.discount_applied = discount


            for line in order.order_line:
                line.discount = discount 
