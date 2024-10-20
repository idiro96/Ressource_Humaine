from odoo import models, fields, api, _



class FicheInformationReport(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_information_report'

    @api.model
    def get_report_values(self, docids, data=None):

        employees= self.env['hr.employee'].browse(docids)



        report_data = {
            'company': self.env.user.company_id,
            "employee": employees,


        }

        return report_data
