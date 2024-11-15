"""pos custom tips"""
# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wb_sample_button_percentage = fields.Float(
        string="WB Sample Button Percentage",
        help="Enter the percentage for the WB Sample Button action.",
        default=0.0
    )

    def set_values(self):
        """Override to store the value entered in the settings."""
        super(ResConfigSettings, self).set_values()
        # Store the WB Sample Button percentage in the pos.config model
        self.env['pos.config'].sudo().write({
            'wb_sample_button_percentage': self.wb_sample_button_percentage,
        })

    @api.model
    def get_values(self):
        """Override to retrieve the value from pos_config."""
        res = super(ResConfigSettings, self).get_values()
        # Get the WB Sample Button percentage from the pos.config model
        pos_config = self.env['pos.config'].sudo().search([], limit=1)
        res.update(
            wb_sample_button_percentage=pos_config.wb_sample_button_percentage if pos_config else 0.0,
        )
        return res
2
