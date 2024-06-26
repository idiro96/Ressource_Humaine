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
        emp_budget = []
        for rec in budget_comptabilite:
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
            emp_budget.append(employee_data)

        informatique = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الإعلام'),
                                                       ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_info = []
        for rec in informatique:
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
            emp_info.append(employee_data)

        mgx = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الوسائل العامة'),
                                              ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_mgx = []
        for rec in mgx:
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
            emp_mgx.append(employee_data)

        internat = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'النظام الداخلي'),
                                                   ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_internat = []
        for rec in internat:
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
            emp_internat.append(employee_data)

        etude = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', '%مديرية الدرسات%'),
                                                ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_etude = []
        for rec in etude:
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
            emp_etude.append(employee_data)

        stage = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التربصات'),
                                                ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_stage = []
        for rec in stage:
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
            emp_stage.append(employee_data)

        formation = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التكوين'),
                                                    ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_formation = []
        for rec in formation:
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
            emp_formation.append(employee_data)

        recherche = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'البحث'),
                                                    ('fin_relation', '=', False)], order='categorie_grade_indice desc')
        emp_recherche = []
        for rec in recherche:
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
            emp_recherche.append(employee_data)

        enseignant = self.env['hr.employee'].search([('department_id', '=', False), ('fin_relation', '=', False),
                                                     ('grade_id.intitule_grade', 'ilike', '%أستاذ%')], order='categorie_grade_indice desc')
        emp_enseignant = []
        for rec in enseignant:
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
            emp_enseignant.append(employee_data)

        report_data = {
            'company': self.env.user.company_id,
            'ressource_humaine': emp_rh,
            'budget_comptabilite': emp_budget,
            'informatique': emp_info,
            'mgx': emp_mgx,
            'internat': emp_internat,
            'etude': emp_etude,
            'stage': emp_stage,
            'formation': emp_formation,
            'recherche': emp_recherche,
            'enseignant': emp_enseignant,
        }

        return report_data
