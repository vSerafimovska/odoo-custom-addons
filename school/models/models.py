# -*- coding: utf-8 -*-
from odoo import fields, models, api
import time



class School(models.Model):
    _name = "wb.school"
    _description = "This is school profile."

    school_image = fields.Image("School Image", max_width=128, max_height=128)
    name = fields.Char("Name")
    invoice_id = fields.Many2one("account.move")
    invoice_user_id = fields.Many2one("res.users", related="invoice_id.invoice_user_id", store=True)
    invoice_date = fields.Date(related="invoice_id.invoice_date")
    student_list = fields.One2many("wb.student", "school_id", string="Students")
    ref_field_id = fields.Reference(selection=[('wb.school', 'School'),
                                     ('wb.student', 'Student'),
                                     ('wb.hobby', 'Hobby'),
                                     ('sale.order', 'Sales'),
                                     ('account.move', 'Invoice'),
                                     ('purchase.order', 'Purchase')], string="reference")

    binary_field = fields.Binary("Upload File")
    binary_file_name = fields.Char("Binay File Name")
    binary_fields = fields.Many2many("ir.attachment", string="Multi files upload")
    my_currency_id = fields.Many2one("res.currency", " My Currency")
    # currency_id = fields.Many2one("res.currency", "Currency")
    amount = fields.Monetary("Amount", currency_field="my_currency_id")

    # def create(self, vals):
    #     print(self)
    #     print(vals)
    #     rtn = super(School, self).create(vals)
    #     print(rtn)
    #     return rtn

    @api.model
    def create(self, vals):
        print(self)
        print(vals)
        rtn = super(School, self).create(vals)
        print(rtn)
        return rtn

    def custom_school_method(self):
        print("Custom school method clicked")
        print(self)


        student_group_by_school = self.env["wb.student"].read_group([],
                                           ["school_id"],
                                         ["school_id"])

        for stud in student_group_by_school:
            print(stud)

       # print(self.read())
       #  abc = self.env["wb.student"].search([])
       #  print(abc.read(fields=["name","school_id"], load = None))
       #  print(abc)

        # total_records = self.env["wb.student"].search_count([])
        # print(total_records)

       # records = self.search([("amount","<","100")])
       # records = self.search([("name","like","Weblearns")])

        # records = self.env["stock.location"].search([("location_id", "parent_of", 22)])
        # self.print_locations(records)

        # records = self.env["wb.student"].search([("school_id", "=", 9)])
        # records = self.env["res.partner"].search(['|',("name", "!=", False),
        #                                           ("phone",'=', False),
        #                                           ("mobile",'=', False)])
        # self.print_table(records)

        # self.name = "Single update"
        # self.amount = 50

        # print(self)
        # print(self.search([], limit=5, offset=1))
        # print(self.env["wb.student"].search([]))
        # print(self.search([("name","ilike","web")]))
        # pass
    # def write(self, vals):
    #     print("Write method called")
    #     print(self)
    #     print(vals)
    #     rtn = super(School, self).write(vals)
    #     print(rtn)
    #     return rtn


    def print_table(self, records):
        print(f"Total Record Found :- {len(records)}")
        print("ID           Name                  Phone           MObile             email")
        for rec in records:
            print(f"{rec.id}            {rec.name}                  {rec.phone}            {rec.mobile}           {rec.email}")
        print("")
        print("")

    def print_locations(self, records):
        print(f"Total Record Found :- {len(records)}")
        print("ID           Name                    Parent")
        for rec in records:
            print(f"{rec.id}            {rec.name}                  {rec.location_id.name} / {rec.location_id.id}")
        print("")
        print("")


    def unlink(self):
        print("Unlink method called")
        print(self)
        rtn = super(School, self).unlink()
        print(rtn)
        print("Unlink method logic finished")
        return rtn



