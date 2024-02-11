from odoo import models, fields, api, _


class ListeNominatifs(models.TransientModel):

    _name = 'liste.nominatifs'


    @api.multi

    def print_report(self):
        return self.env.ref('ressource_humaine.action_liste_nominatife').report_action(self)


class PlanningCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_nominatife_employee'

    @api.model
    def get_report_values(self, docids, data=None):
        # conge = self.env['planning.conge'].browse(docids[0])
        employee_sup = self.env['hr.employee'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieure')])
        employee_post_sup = self.env['hr.employee'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure')])
        employee_enseignant = self.env['hr.employee'].search([('grade_id.intitule_grade', 'like', 	'%أستاذ%')])
        employee_pleintemps_indeterminee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'pleintemps_indeterminee')])
        employee_pleintemps_determinee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'pleintemps_determinee')])
        employee_partiel_indeterminee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'partiel_indeterminee')])
        employee_partiel_determinee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'partiel_determinee')])

        employees = self.env['hr.employee'].browse(docids[0])

        report_data = {
            # 'conge': conge,
            'company': self.env.user.company_id,
            'employee_sup': employee_sup,
            'employee_post_sup': employee_post_sup,
            'employee_enseignant': employee_enseignant,
            'employee_pleintemps_indeterminee': employee_pleintemps_indeterminee,
            'employee_pleintemps_determinee': employee_pleintemps_determinee,
            'employee_partiel_indeterminee': employee_partiel_indeterminee,
            'employee_partiel_determinee': employee_partiel_determinee,
        }

        return report_data
