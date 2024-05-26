from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AttestationTravailReport(models.AbstractModel):
    _name = 'report.ressource_humaine.renew_contract_report'

    @api.model
    def get_report_values(self, docids, data=None):
        contract = self.env['hr.contract'].browse(docids[0])

        formatted_date_start = None
        if contract.date_start:
            report_date_start = contract.date_start
            formatted_date_start = datetime.strptime(report_date_start, "%Y-%m-%d").strftime("%Y/%m/%d")

        report_data = {
            'contract': contract,
            'company': self.env.user.company_id,
            'formatted_date_start': formatted_date_start,
        }

        return report_data
