# -*- coding: utf-8 -*-
{
    'name': "fields_functions_jarochito",

    'summary': """
        Fields, reports, functions and labels""",

    'description': """
        Add fields in contacts and sales, as well as in reports, create labels for 
        pallets and select the type of rate of the shipping address
    """,

    'author': "Xmarts",
    'Collaborator' : "Marco Aguilar",
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contacts, sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','stock','contacts','point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu_items.xml',
        'views/sale_order_view.xml',
        #'reports/fields_in_report.xml',
        #'reports/layout.xml',
        #'reports/print_pallets.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False
}