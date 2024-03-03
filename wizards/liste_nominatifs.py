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
        job_sup = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieure')])
        supp_employees = []
        for job in job_sup:
            employees = self.env['hr.employee'].search([('job_id', '=', job.id)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                supp_employees.append({'job': job, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                supp_employees.append({'job': job, 'employees': employees, 'promotion_lines': None})

        job_hight = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure')])
        hight_employees = []
        for job in job_hight:
            employees = self.env['hr.employee'].search([('job_id', '=', job.id)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                hight_employees.append({'job': job, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                hight_employees.append({'job': job, 'employees': employees, 'promotion_lines': None})

        grade_enseignant = self.env['rh.grade'].search([('intitule_grade', 'ilike', '%أستاذ%')])
        enseignant_employees = []
        for grade in grade_enseignant:
            employees = self.env['hr.employee'].search([('grade_id', '=', grade.id)])
            promotion_lines = self.env['rh.promotion.line'].search([('employee_id', 'in', employees.ids)],
                                                                   order='date_new_grade DESC', limit=1)
            if promotion_lines:
                enseignant_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': promotion_lines})
            else:
                enseignant_employees.append({'grade': grade, 'employees': employees, 'promotion_lines': None})

        employee_enseignant = self.env['hr.employee'].search([('grade_id.intitule_grade', 'ilike', '%أستاذ%')])
        employee_grade_a = self.env['hr.employee'].search([('grade_id.categorie_id.groupe_id.name', 'ilike', 'المجموعة أ')])
        employee_grade_a_excluded = employee_grade_a - employee_enseignant
        employee_grade_b = self.env['hr.employee'].search([('grade_id.categorie_id.groupe_id.name', 'ilike', 'المجموعة ب')])
        employee_grade_c = self.env['hr.employee'].search([('grade_id.categorie_id.groupe_id.name', 'ilike', 'المجموعة ج')])
        employee_grade_d = self.env['hr.employee'].search([('grade_id.categorie_id.groupe_id.name', 'ilike', 'المجموعة د')])
        employee_pleintemps_indeterminee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'pleintemps_indeterminee')])
        employee_pleintemps_determinee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'pleintemps_determinee')])
        employee_partiel_indeterminee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'partiel_indeterminee')])
        employee_partiel_determinee = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 	'partiel_determinee')])

        employees = self.env['hr.employee'].browse(docids[0])

        report_data = {
            'company': self.env.user.company_id,
            'job_sup': supp_employees,
            'job_hight': hight_employees,
            'grade_enseignant': enseignant_employees,
            'employee_enseignant': employee_enseignant,
            'employee_grade_a_excluded': employee_grade_a_excluded,
            'employee_grade_b': employee_grade_b,
            'employee_grade_c': employee_grade_c,
            'employee_grade_d': employee_grade_d,
            'employee_pleintemps_indeterminee': employee_pleintemps_indeterminee,
            'employee_pleintemps_determinee': employee_pleintemps_determinee,
            'employee_partiel_indeterminee': employee_partiel_indeterminee,
            'employee_partiel_determinee': employee_partiel_determinee,
        }

        return report_data
