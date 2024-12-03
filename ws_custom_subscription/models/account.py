from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_account_income_id = fields.Many2one('account.account', string="Custom Income Account")
