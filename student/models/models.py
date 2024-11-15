# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError
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
    ref_field_id = fields.Reference(selection=[('wb.school','School'),
                                     ('wb.student','Student'),
                                     ('wb.hobby','Hobby'),
                                     ('sale.order','Sales'),
                                     ('account.move','Invoice'),
                                     ('purchase.order','Purchase')], string="reference")

    binary_field = fields.Binary("Binary field")
    binary_file_name = fields.Char("Upload File")
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

    # def write(self, vals):
    #     print("Write method called")
    #     print(self)
    #     print(vals)
    #     rtn = super(School, self).write(vals)
    #     print(rtn)
    #     return rtn

    def custom_school_method(self):
        print("Custom school method clicked")

        records = self.search([("amount", "=", "100")])
        self.print_table(records)
        # print(self)

        # self.name = "Single update"
        # self.amount = 50
        # pass

    def print_table(self, records):
        print(f"Total Record Found :- {len(records)}")
        print("ID           Name                    Amount")
        for rec in records:
            print(f"{rec.id}            {rec.name}                  {rec.amount}")
        print("")
        print("")

    def unlink(self):
        print("Unlink method called")
        print(self)
        rtn = super(School, self).unlink()
        print(rtn)
        print("Unlink method logic finished")
        return rtn

class Hobby(models.Model):
    _name = "wb.hobby"
    _description = "This is hobby profile."

    name = fields.Char("Name")


class Student(models.Model):
    _name = "wb.student"
    _description = "This is student profile."

    def delete_records(self):
        print(self)


        school_record = self.env["wb.school"].browse(45)


        if school_record.exists():

            is_deleted = school_record.unlink()
            print(f"Record deleted: {is_deleted}")  # Output will be True if deletion is successful
        else:
            raise UserError(f"Record set is not available {school_record}")
            print("instance or record is not available.")




    def duplicate_records(self):
        print(self)
        duplicate_record = self.copy()
        print(duplicate_record)


    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        print(self)
        print(default)
        rtn = super(Student, self).copy(default=default)
        print(rtn)
        return rtn




    hobby_list = fields.Many2many("wb.hobby","student_hobby_list_relation","student_id","hobby_id")
    # hobby_list_ids = fields.Many2many("wb.hobby")
    school_id = fields.Many2one(comodel_name="wb.school", string="schoool", help="enter school id")
    joining_date = fields.Datetime("Join date!", default=fields.Datetime.now(), copy=False)


    # joining_date = fields.Date("Date", default=fields.Date.today())
    #
    # start_date = fields.Date(default=time.strftime("%Y-01-01"))
    # end_date = fields.Date(default=time.strftime("%Y-12-31"))

    school_data = fields.Json("JSON FEED")

    @api.model

    def _get_vip_list(self):
        return [('a','A'), ('b','B')]

    gender = fields.Selection(
        [('male','Male'), ('female','Female')]
    )

    advance_gender = fields.Selection("get_gender_list")
    vip_gender=fields.Selection("_get_vip_list")

    student_fees = fields.Float("Student total fees", default=3.2, help="help", index=True)
    discount_fees = fields.Float("Discount")

    roll_number = fields.Integer("Roll NUmber 2")

    is_default = fields.Boolean(default=True)
    is_paid = fields.Boolean(" ->Paid?", help="this is for help", default="True")
    name = fields.Char("Name")
    name1 = fields.Char("Name1")
    name2 = fields.Char("Name2")
    name3 = fields.Char("Name3")
    name4 = fields.Char("Name4")

    student_name = fields.Char("STD", size=5)
    address = fields.Text("Student Address Label", help="Enter here student address", default="Hello student address...")

    address_html = fields.Html(string="Address HTML Field",
                               #required=1,
                               #default="<h1>This is the default value from backend<h1/>",
                               help="field for help",
                               copy="False")

    final_fees = fields.Float("Final Fees", compute="_compute_final_fees_calc", store=True)

    compute_address_html = fields.Html(string="Compute address field")

    @api.onchange("address_html")

    def onchange_address_html_field(self):
        for record in self:
            record.compute_address_html = record.address_html


    @api.onchange("student_fees","discount_fees")
    def _compute_final_fees_calc(self):
        for record in self:
            record.final_fees = record.student_fees - record.discount_fees

    def get_gender_list(self):
        return [('male','Male'),
                ('female','Female')]

    def json_data_store(self):
        self.school_data = {"name":self.name, "id":self.id, "fees":self.student_fees, "g":self.gender}


    def custom_method(self):
        print("Clicked!")

        data = [{"name":"Weblearns record 1"},
                {"name":"Weblearns record 2"},
                {"name":"Weblearns record 3"},
                {"name":"Weblearns record 4"}]

        self.env["wb.school"].create(data)