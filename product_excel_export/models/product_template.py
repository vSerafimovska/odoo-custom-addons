from odoo import models
import base64
from io import BytesIO
import xlsxwriter
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_export_excel(self):
        _logger.info("Export Excel button clicked!")


        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()


        worksheet.write(0, 0, "Product Name")
        worksheet.write(0, 1, "Product Price")


        products = self.search([])
        row = 1
        for product in products:
            worksheet.write(row, 0, product.name)
            worksheet.write(row, 1, product.list_price)
            row += 1

        workbook.close()


        output.seek(0)
        excel_file = base64.b64encode(output.read())
        attachment = self.env["ir.attachment"].create(
            {
                "name": "products_report.xlsx",
                "type": "binary",
                "datas": excel_file,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "new",
        }
