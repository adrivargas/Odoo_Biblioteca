# -*- coding: utf-8 -*-
{
    'name': "biblioteca",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

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
    'depends': ['base'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/views_libro.xml',
        'views/views_prestamo.xml',
        'views/views_personas.xml',
        # 'views/views_detallePrestamo',
        'views/views_categoria.xml',
        'views/views_tipo.xml',
        'data/users_group.xml',
        'security/ir.model.access.csv'
        # 'views/views_detallePrestamo.xml'
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}

