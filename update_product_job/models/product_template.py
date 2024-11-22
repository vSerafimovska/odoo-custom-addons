from odoo import models, fields, api
import random
import string
import logging

_logger = logging.getLogger(__name__)

DEFAULT_TAX_GROUP = 'General Sales Taxes'
DEFAULT_PRICE = 10.1


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_storable = fields.Boolean(string="Is Storable?", default=True)
    barcode_value = fields.Char("Barcode", help="The barcode value for the product")

    def action_enqueue_job(self):
        for product in self:
            _logger.info("Action clicked for product: %s", product.name)

            now = fields.Datetime.now()
            barcode_value = product.generate_barcode()

            taxes_values = (4, product._get_or_create_tax('19%', 19.0, 'sale').id)
            supplier_taxes_values = (4, product._get_or_create_tax('15%', 15.0, 'purchase').id)

            values = product._prepare_product_values(now, taxes_values, supplier_taxes_values, barcode_value)
            _logger.debug("Values being passed: %s", values)

            product.with_delay().update_product_job(values)

    def _get_or_create_tax(self, name, amount, tax_use):
        tax = self.env['account.tax'].search([('name', '=', name)], limit=1)
        if not tax:
            tax_group = self.env['account.tax.group'].search([('name', '=', DEFAULT_TAX_GROUP)], limit=1)
            if not tax_group:
                tax_group = self.env['account.tax.group'].create({'name': DEFAULT_TAX_GROUP})

            tax = self.env['account.tax'].create({
                'name': name,
                'amount': amount,
                'type_tax_use': tax_use,
                'tax_group_id': tax_group.id,
                'amount_type': 'percent',
            })
            _logger.info("Tax '%s' created.", name)
        return tax

    def _prepare_product_values(self, now, taxes_values, supplier_taxes_values, barcode_value):
        return {
            "name": f"Product 1 {now}",
            "description_sale": f"This is the description after the job run + exact timedate of clicking {now}",
            "list_price": DEFAULT_PRICE,
            "barcode": barcode_value,
            "is_storable": True,
            "taxes_id": taxes_values,
            "supplier_taxes_id": supplier_taxes_values
        }

    def update_product_job(self, values):
        if not isinstance(values, dict):
            raise ValueError("Values must be dictionaries")
        self.validate_product_values(values)
        self.write(values)
        _logger.info("Product updated with new values: %s", self.name)

    def validate_product_values(self, values):
        if not values.get('name'):
            raise ValueError("Product name is required.")
        if values.get('list_price', 0) < 0:
            raise ValueError("List price cannot be negative.")
        return True

    def generate_barcode(self):
        return ''.join(random.choices(string.digits, k=12))
