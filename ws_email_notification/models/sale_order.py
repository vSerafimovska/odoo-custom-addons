from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, values):

        order = super(SaleOrder, self).create(values)


        if order.state == 'sale':  
            self._send_confirmation_email(order)

        return order

    def _send_confirmation_email(self, order):
        template = self.env.ref('my_email_notification.email_template_sale_order')
        if template:
            template.send_mail(order.id, force_send=True)
