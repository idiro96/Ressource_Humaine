from odoo import models, fields, api, _


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

        report_data = {
            'company': self.env.user.company_id,
            'job_supp': job_supp,
            'job_hight_org': job_hight_org,
            'job_hight_squ': job_hight_squ,
        }

        return report_data
