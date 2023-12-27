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

    'depends': ['base','hr'],


    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        # 'views/views.xml',
        # 'views/templates.xml',
        # 'views/data.xml',

        'views/hr_employee_inherit.xml',
        'views/hr_holidays_inherit.xml',
        'views/conjoint.xml',
        'views/hr_contrat_inherit.xml',
        'views/type_contrat.xml',
        'views/fin_relation.xml',
        'views/formation.xml',
        'views/organisme.xml',
        'views/type_formation.xml',
        'views/type_fin_relation.xml',
        'views/visite_medicale.xml',
        'views/enfant.xml',
        'views/cabinet_medical.xml',
        'views/sanction.xml',
        'views/absence.xml',
        'views/type_sanction.xml',
        'views/type_faute.xml',
        'views/type_absence.xml',
        'views/absence.xml',
        'views/accident_travail.xml',
        'views/hr_holidays_inherit.xml',
        'views/type_file.xml',
        'views/conge_droit.xml',
        'views/cron_view.xml',
        'views/grille.xml',
        'views/hr_job_inherit.xml',
        'views/Loi.xml',
        'views/filiere.xml',
        'views/corps.xml',
        'views/grade.xml',
        'views/promotion.xml',
        'views/nature_travail.xml',
        'data/sequence.xml',
        'wizards/visite_medical_detaille.xml',
        'wizards/formation_detail_wizard.xml',
        'wizards/formation_absence_wizard.xml',
        'wizards/choisir_commission.xml',
        'reports/hr_contract.xml',
        'reports/attestation_travail.xml',
        'reports/attestation_travail_fr.xml',
        'reports/cont_indete_tem_part.xml',
        'reports/report_rh.xml',
        'reports/titre_conge.xml',
        'reports/report_template_header.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
}