from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_subscription = fields.Boolean(string="Is Subscription", default=False)
    subscription_start_date = fields.Date(string="Subscription Start Date")
    subscription_end_date = fields.Date(string="Subscription End Date")
    subscription_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string="Subscription Frequency")
    subscription_journal_id = fields.Many2one('account.journal', string="Subscription Journal")

    def trigger_subscription_job(self):
        for order in self:
            now = fields.Datetime.now()
            job_description = f"Processing subscription ({order.name}) at {now.strftime('%m/%d/%Y %H:%M:%S')}"
            order.with_delay(description=job_description).process_subscription_invoices()

    def process_subscription_invoices(self):
        for subscription in self:
            try:

                journal = subscription.subscription_journal_id or self.env.ref(
                    'account.account_journal_sale', raise_if_not_found=False
                )
                if not journal:
                    raise UserError("No valid journal found for the subscription invoice.")


                order_line = subscription.order_line.filtered(lambda line: line.product_id)
                if not order_line:
                    raise UserError("No product found in the order.")

                product = order_line[0].product_id


                income_account = product.product_tmpl_id.custom_account_income_id or product.product_tmpl_id.property_account_income_id

                if not income_account:

                    fallback_account = self.env['account.account'].search([
                        ('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)
                    ], limit=1)

                    if not fallback_account:
                        raise UserError(
                            "No default income account found in the system. Please configure at least one income account."
                        )

                    income_account = fallback_account


                invoice_vals = {
                    'partner_id': subscription.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'journal_id': journal.id,
                    'invoice_line_ids': [(0, 0, {
                        'product_id': product.id,
                        'quantity': 1,
                        'price_unit': product.list_price,
                        'account_id': income_account.id,
                    })],
                }

                # Create and post invoice
                invoice = self.env['account.move'].create(invoice_vals)
                invoice.action_post()

                _logger.info(f"Invoice {invoice.id} created and posted successfully for Sale Order {subscription.name}")


                job = self.env.context.get('queue_job', False)
                if job:
                    job._set_state('done')

            except Exception as e:
                
                _logger.error(f"Error processing subscription invoice for Sale Order {subscription.name}: {str(e)}")

                job = self.env.context.get('queue_job', False)
                if job:
                    job._set_state('failed')
                    job._set_error(str(e))

                raise e



