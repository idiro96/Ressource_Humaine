from datetime import datetime

from odoo import models, fields, api, _


class OrganizationChartReport(models.AbstractModel):
    _name = 'report.ressource_humaine.prime_rendement_report'

    @api.model
    def get_report_values(self, docids, data=None):
        prime_rendement = self.env['rh.prime.rendement'].browse(docids[0])
        ressource_humaine = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                                        ('employee_id.department_id.complete_name',
                                                                         'ilike', 'الموارد البشرية')],
                                                                       order='categorie_grade_indice desc')

        budget_comptabilite = self.env['rh.prime.rendement.line'].search(
            [('prime_rendement_id', '=', prime_rendement.id),
             ('employee_id.department_id.complete_name',
              'ilike', 'الميزانية')], order='categorie_grade_indice desc')

        informatique = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                                   ('employee_id.department_id.complete_name',
                                                                    'ilike', 'الإعلام')], order='categorie_grade_indice desc')

        mgx = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                          ('employee_id.department_id.complete_name',
                                                           'ilike', 'الوسائل العامة')], order='categorie_grade_indice desc')

        internat = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                               ('employee_id.department_id.complete_name',
                                                                'ilike', 'النظام الداخلي')], order='categorie_grade_indice desc')

        etude = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                            ('employee_id.department_id.complete_name',
                                                             'ilike', '%مديرية الدرسات%')], order='categorie_grade_indice desc')

        stage = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                            ('employee_id.department_id.complete_name',
                                                             'ilike', 'التربصات')], order='categorie_grade_indice desc')

        formation = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                                ('employee_id.department_id.complete_name',
                                                                 'ilike', 'التكوين')], order='categorie_grade_indice desc')

        recherche = self.env['rh.prime.rendement.line'].search([('prime_rendement_id', '=', prime_rendement.id),
                                                                ('employee_id.department_id.complete_name',
                                                                 'ilike', 'البحث')], order='categorie_grade_indice desc')

        report_data = {
            'prime_rendement': prime_rendement,
            'trimestre': self.get_trimestre(prime_rendement.date_fin),
            'company': self.env.user.company_id,
            'ressource_humaine': ressource_humaine,
            'budget_comptabilite': budget_comptabilite,
            'informatique': informatique,
            'mgx': mgx,
            'internat': internat,
            'etude': etude,
            'stage': stage,
            'formation': formation,
            'recherche': recherche,
        }

        return report_data

    def get_trimestre(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj.month == 3 and date_obj.day == 31:
            return 'الأول'
        elif date_obj.month == 6 and date_obj.day == 30:
            return 'الثاني'
        elif date_obj.month == 9 and date_obj.day == 30:
            return 'الثالث'
        elif date_obj.month == 12 and date_obj.day == 31:
            return 'الرابع'
        else:
            return 'التاريخ لا يطابق أي نهاية ثلاثي'
