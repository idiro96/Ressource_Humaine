from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TableauPromotionReport(models.AbstractModel):

    _name = 'report.ressource_humaine.tableau_promotion'

    @api.model
    def get_report_values(self, docids, data=None):
        avencement_droit = self.env['rh.avencement.droit'].browse(docids[0])

        report_data = {
            'avencement_droit': avencement_droit,
            'company': self.env.user.company_id,
        }

        return report_data
