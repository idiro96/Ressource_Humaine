# -*- coding: utf-8 -*-
{
    'name': "ressource_humaine",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly

    'depends': ['base', 'hr', 'hr_recruitment', 'hr_holidays', 'board' ],

    # 'depends': ['base', 'hr'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/hr_employee_inherit.xml",
        'views/type_fonction.xml',
        'views/categorie_superieure.xml',
        'views/company.xml',
        'views/critere.xml',
        'views/emphy.xml',
        'views/hr_job_inherit.xml',
        'views/Loi.xml',
        'views/planning_surveillance.xml',
        'views/section_superieure.xml',
        'views/type_absence.xml',
        'views/type_conge.xml',
        'views/type_faute.xml',
        'views/type_file.xml',
        'views/type_fin_relation.xml',
        'views/type_formation.xml',
        'views/type_sanction.xml',
        'views/conjoint.xml',
        'views/accident_travail.xml',
        'views/enfant.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
