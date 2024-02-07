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

        employees = self.env['hr.employee'].browse(docids[0])

        report_data = {
            # 'conge': conge,
            'company': self.env.user.company_id,
            'employees': employees,
        }

        return report_data
