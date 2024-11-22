# -*- coding: utf-8 -*-
{
    'name': "Point of Sale",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'sequence':10,

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [

    ],

'assets': {
    'point_of_sale.assets': [
        'wb_pos/static/src/js/wb_sample_button.js',
        'wb_pos/static/src/xml/wb_sample_button.xml',
    ],
},


}

