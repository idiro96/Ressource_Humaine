from odoo import models, fields, api, _
from itertools import groupby


class ListeNominative(models.TransientModel):
    _name = 'liste.nominative'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_liste_nominative').report_action(self)


class ListeNominativeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_nominative'

    @api.model
    def get_report_values(self, docids, data=None):
        job_supp = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'postesuperieure')])
        job_hight_org = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                                   ('poste_organique', '=', 'organique')])
        job_hight_squ = self.env['hr.job'].search([('nature_travail_id.code_type_fonction', '=', 'fonctionsuperieure'),
                                                   ('poste_organique', '=', 'squelaire')])

        contract_jobs = self.env['hr.contract'].search([('type_id.code_type_contract', '=', 'pleintemps_indeterminee'),
                                                        ('employee_id.job_id', '!=', False)])

        grouped_jobs = {}
        for contract in contract_jobs:
            job_id = contract.job_id.id
            if job_id not in grouped_jobs:
                grouped_jobs[job_id] = contract
            else:
                if contract.create_date < grouped_jobs[job_id].create_date:
                    grouped_jobs[job_id] = contract

        first_records = list(grouped_jobs.values())
        print(first_records)

        grade_proff = self.env['rh.grade'].search([('intitule_grade', 'ilike', 'أستاذ')])
        grade_a = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة أ')])
        grade_a_excluded = grade_a - grade_proff
        grade_b = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ب')])
        grade_c = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة ج')])
        grade_d = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د')])
        grade_d_2 = self.env['rh.grade'].search([('categorie_id.groupe_id.name', 'ilike', 'المجموعة د'),
                                                 ('intitule_grade', 'ilike', 'مهن')])
        grade_d_1 = grade_d - grade_d_2

        report_data = {
            'company': self.env.user.company_id,
            'job_supp': job_supp,
            'job_hight_org': job_hight_org,
            'job_hight_squ': job_hight_squ,
            'first_records': first_records,
            'grade_proff': grade_proff,
            'grade_a_excluded': grade_a_excluded,
            'grade_b': grade_b,
            'grade_c': grade_c,
            'grade_d_1': grade_d_1,
            'grade_d_2': grade_d_2,
        }

        return report_data
