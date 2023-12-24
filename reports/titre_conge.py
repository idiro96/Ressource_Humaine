from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TitreCongeReport(models.AbstractModel):
    _name = 'report.ressource_humaine.titre_conge'

    @api.model
    def get_report_values(self, docids, data=None):
        conge = self.env['hr.holidays'].browse(docids[0])

        contract = self.env['hr.contract'].search([('employee_id', '=', conge.employee_id.id)], limit=1)

        conge_date_to = fields.Date.from_string(conge.date_to)
        conge_date_from = fields.Date.from_string(conge.date_from)

        report_data = {
            'conge': conge,
            'company': self.env.user.company_id,
            'contract': contract,
            'conge_date_to': conge_date_to,
            'conge_date_from': conge_date_from,
        }

        return report_data
