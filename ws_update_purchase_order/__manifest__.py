{
    'name': 'Update Purchase Order',
    'summary': 'Adds a button to purchase orders for updating details with a background job',
    'license': 'AGPL-3',
    'version': '0.1',
    'category': 'Purchases',
    'author': '',
    'website': '',
    'depends': ['purchase', 'queue_job', 'account'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': False,

}