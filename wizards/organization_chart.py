import re

from odoo import models, fields, api, _


class OrganizationChart(models.TransientModel):
    _name = 'organization.chart'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_organization_chart').report_action(self)


class OrganizationChartReport(models.AbstractModel):
    _name = 'report.ressource_humaine.organization_chart_report'

    @api.model
    def get_report_values(self, docids, data=None):
        ressource_humaine = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الموارد البشرية'),
                                                            ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_rh = []
        for rec in ressource_humaine:
            department_name = rec.department_id.name
            if department_name:
                department_name = re.sub(r'^(مكتب|مصلحة)\s*', '', department_name).strip()
            employee_data = {
                'name': rec.name,
                'birthday': rec.birthday,
                'place_of_birth': rec.place_of_birth,
                'grade': rec.grade_id.intitule_grade,
                'description': rec.grade_id.description,
                'job_name': rec.job_id.name,
                'job_type': rec.job_id.poste_organique,
                'department_name': department_name,
            }
            emp_rh.append(employee_data)

        budget_comptabilite = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الميزانية'),
                                                              ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        informatique = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الإعلام'),
                                                       ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        mgx = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الوسائل العامة'),
                                              ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        internat = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'النظام الداخلي'),
                                                   ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        etude = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', '%مديرية الدرسات%'),
                                                ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        stage = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التربصات'),
                                                ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        formation = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التكوين'),
                                                    ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        recherche = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'البحث'),
                                                    ('fin_relation', '=', False)], order='categorie_grade_indice desc')

        enseignant = self.env['hr.employee'].search([('department_id', '=', False), ('fin_relation', '=', False),
                                                     ('grade_id.intitule_grade', 'ilike', '%أستاذ%')], order='categorie_grade_indice desc')

        report_data = {
            'company': self.env.user.company_id,
            'ressource_humaine': emp_rh,
            'budget_comptabilite': budget_comptabilite,
            'informatique': informatique,
            'mgx': mgx,
            'internat': internat,
            'etude': etude,
            'stage': stage,
            'formation': formation,
            'recherche': recherche,
            'enseignant': enseignant,
        }

        return report_data
