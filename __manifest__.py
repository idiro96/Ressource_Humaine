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

    'depends': ['base', 'hr', 'hr_recruitment', 'hr_holidays', 'hr_payroll', 'board', 'web_responsive',
                'enterprise_theme',
                'web_rtl', 'website_rtl', 'report_xlsx', 'field_timepicker'],

    # always loaded
    'data': [
        'security/ressource_humaine_security.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        # 'views/data.xml',
        'wizards/droit_avencement.xml',
        'wizards/droit_promotion.xml',
        'views/hr_dashboard.xml',
        'views/templates.xml',
        'views/hr_employee_inherit.xml',
        'views/hr_holidays_inherit.xml',
        'views/conjoint.xml',
        'views/hr_contrat_inherit.xml',
        'views/fin_relation.xml',
        'views/formation.xml',
        'views/organisme.xml',
        'views/type_formation.xml',
        'views/type_fin_relation.xml',
        'views/visite_medicale.xml',
        'views/enfant.xml',
        'views/cabinet_medical.xml',
        'views/grille.xml',
        'views/sanction.xml',
        # 'views/assets.xml',
        'views/type_sanction.xml',
        'views/type_faute.xml',
        'views/type_absence.xml',
        'views/accident_travail.xml',
        'views/hr_holidays_inherit.xml',
        'views/type_file.xml',
        'views/hr_contract_type_inherit.xml',
        'views/absence.xml',
        'wizards/droit_conge.xml',
        'views/conge_droit.xml',
        'views/cron_view.xml',
        'views/hr_job_inherit.xml',
        'views/groupe.xml',
        'views/categorie.xml',
        'views/categorie_superieure.xml',
        'views/echelon.xml',
        'views/niveau_hierarchique.xml',
        'views/niveau_hierarchique_chef_bureau.xml',
        'views/section.xml',
        'views/section_superieure.xml',
        'views/type_fonction.xml',
        'views/promotion.xml',
        'views/Loi.xml',
        'views/filiere.xml',
        'views/corps.xml',
        'views/grade.xml',
        'views/fiche_evaluation.xml',
        'views/avancement.xml',
        'views/avencement_droit.xml',
        'views/promotion_droit.xml',
        'views/company.xml',
        'views/emphy.xml',
        'views/planning_surveillance.xml',
        'data/sequence.xml',
        'data/type_fonction.xml',
        'data/type_contract.xml',
        'data/type_file.xml',
        'data/type_fin_relation.xml',
        'wizards/visite_medical_detaille.xml',
        'wizards/formation_detail_wizard.xml',
        'wizards/choisir_commission.xml',
        'wizards/commission_avancement.xml',
        'wizards/commission_promotion.xml',
        'wizards/planning_choix.xml',
        'wizards/planning_conge.xml',
        'wizards/liste_nominatife.xml',
        'wizards/liste_nominative.xml',
        'wizards/attestation_travail_wizard.xml',
        'wizards/programme_surveillance_employee.xml',
        'wizards/organization_chart.xml',
        'reports/paper_format.xml',
        'reports/hr_contract.xml',
        'reports/attestation_travail.xml',
        'reports/attestation_travail_fr.xml',
        'reports/cont_indete_tem_part.xml',
        'reports/report_rh.xml',
        'reports/titre_conge.xml',
        'reports/report_template_header.xml',
        'reports/cnas_header.xml',
        'reports/note_conge.xml',
        'reports/pv_instalation.xml',
        'reports/planning_conge.xml',
        'reports/contract_renew.xml',
        'reports/droit_avancement.xml',
        'reports/droit_promotion.xml',
        'reports/tableau_promotion.xml',
        'reports/tableau_des_promotions.xml',
        'reports/liste_employee.xml',
        'reports/planning_surveillance.xml',
        'reports/liste_nominatife_employee.xml',
        'reports/fiche_renseignement.xml',
        'reports/liste_nominative.xml',
        'reports/rapport_retraite_text.xml',
        'reports/attestation_de_cessation.xml',
        'reports/planning_notice.xml',
        'reports/organization_chart.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
}
