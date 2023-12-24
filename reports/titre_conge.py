from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TitreCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.titre_conge'

    @api.model
    def get_report_values(self, docids, data=None):
        conge = self.env['hr.holidays'].browse(docids[0])

        report_data = {
            'conge': conge,
            'company': self.env.user.company_id,
        }

        return report_data
