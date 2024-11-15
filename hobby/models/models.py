# -*- coding: utf-8 -*-
from odoo import fields, models, api
import time



class Hobby(models.Model):
    _name = "wb.hobby"
    _description = "This is hobby profile."

    name = fields.Char("Name")


