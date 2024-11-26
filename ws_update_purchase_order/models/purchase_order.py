from odoo import models, fields
from odoo.exceptions import ValidationError
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )

    VENDOR_NAME = 'Издавачка куќа Сакам Книги'
    TARGET_CURRENCY = 'USD'
    FISCAL_POSITION = 'Rest of the world'
    PAYMENT_TERMS = '30% Now, Balance 60 Days'
    BUYER_NAME = 'Viktorija Serafimovska'

    def action_enqueue_job(self):
        for order in self:
            # Create a description with the order name and current timestamp in reversed format
            now = fields.Datetime.now()
            job_description = f"({order.name}) Update at {now.strftime('%m/%d/%Y %H:%M:%S')}"
            order.with_delay(description=job_description).update_purchase_order()

    def update_purchase_order(self):
        # Fetch necessary records for the update
        vendor = self.env['res.partner'].search([('name', '=', self.VENDOR_NAME)], limit=1)
        currency = self.env['res.currency'].search([('name', '=', self.TARGET_CURRENCY)], limit=1)
        fiscal_position = self.env['account.fiscal.position'].search([('name', '=', self.FISCAL_POSITION)], limit=1)
        payment_term = self.env['account.payment.term'].search([('name', '=', self.PAYMENT_TERMS)], limit=1)
        buyer = self.env['res.users'].search([('name', '=', self.BUYER_NAME)], limit=1)

        if not vendor:
            raise ValidationError(f"Vendor '{self.VENDOR_NAME}' not found.")
        if not currency:
            raise ValidationError(f"Currency '{self.TARGET_CURRENCY}' not found.")

        for order in self:
            # Update order details
            order.write({
                'partner_id': vendor.id,
                'currency_id': currency.id,
                'payment_term_id': payment_term.id if payment_term else False,
                'user_id': buyer.id if buyer else False,
            })

            # Convert and update order line prices if necessary
            for line in order.order_line:
                if order.currency_id != currency:
                    converted_price_unit = order.currency_id._convert(
                        line.price_unit,
                        currency,
                        order.company_id,
                        order.date_order or datetime.now()
                    )
                    converted_price_subtotal = converted_price_unit * line.product_qty
                    line.write({
                        'price_unit': converted_price_unit,
                        'price_subtotal': converted_price_subtotal,
                    })
