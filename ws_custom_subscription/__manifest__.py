{
    'name': 'WS Custom Subscription',
    'version': '0.1',
    'depends': ['sale', 'sale_management', 'account', 'queue_job', 'base'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_template_view.xml',
    ],
    'installable': True,
    'application': False,
}


