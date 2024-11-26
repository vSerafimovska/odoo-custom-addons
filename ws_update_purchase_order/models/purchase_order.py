from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Constants for reusable values
    VENDOR_NAME = 'Издавачка куќа Сакам Книги'
    TARGET_CURRENCY = 'GBP'
    FISCAL_POSITION = 'Rest of the world'
    PAYMENT_TERMS = '30% Now, Balance 60 Days'
    BUYER_NAME = 'Viktorija Serafimovska'

    def action_enqueue_job(self):
        """
        Enqueue a job to update the purchase order with specific details.
        """
        for order in self:
            order.with_delay().update_purchase_order()

    def update_purchase_order(self):
        """
        Updates the purchase order:
        - Sets vendor, currency, fiscal position, payment terms, and buyer.
        - Converts prices and totals to the target currency.
        """

        # Fetch static records
        vendor = self.env['res.partner'].search([('name', '=', self.VENDOR_NAME)], limit=1)
        currency = self.env['res.currency'].search([('name', '=', self.TARGET_CURRENCY)], limit=1)
        fiscal_position = self.env['account.fiscal.position'].search([('name', '=', self.FISCAL_POSITION)], limit=1)
        payment_term = self.env['account.payment.term'].search([('name', '=', self.PAYMENT_TERMS)], limit=1)
        buyer = self.env['res.users'].search([('name', '=', self.BUYER_NAME)], limit=1)

        # Validation for required fields
        if not vendor:
            raise ValidationError(f"Vendor '{self.VENDOR_NAME}' not found.")
        if not currency:
            raise ValidationError(f"Currency '{self.TARGET_CURRENCY}' not found.")

        for order in self:
            # Update the purchase order
            order.write({
                'partner_id': vendor.id,
                'currency_id': currency.id,
                'fiscal_position_id': fiscal_position.id if fiscal_position else False,
                'payment_term_id': payment_term.id if payment_term else False,
                'user_id': buyer.id if buyer else False,
            })

            # Update order line prices
            for line in order.order_line:
                if order.currency_id != currency:
                    converted_price_unit = order.currency_id._convert(
                        line.price_unit, currency, order.company_id, order.date_order or datetime.now()
                    )
                    converted_price_subtotal = converted_price_unit * line.product_qty
                    line.write({
                        'price_unit': converted_price_unit,
                        'price_subtotal': converted_price_subtotal,
                    })
