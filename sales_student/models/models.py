# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError
import time

class SalesStudent(models.Model):
    _name = 'sales.student'
    _description = "This is sales student profile"
    _inherit = 'wb.student'  # Inherit from wb.student

    mobile = fields.Char(string="Mobile")

    hobby_list = fields.Many2many(
        'wb.hobby',
        'student_hobby_rel',
        'student_id',
        'hobby_id',
        string='Hobbies'
    )

    gender = fields.Selection(
        selection_add=[('neutral', 'Neutral')]
    )




