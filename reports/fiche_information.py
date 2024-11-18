from datetime import datetime

from odoo import models, fields, api, _



class FicheInformationReport(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_information_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employees = self.env['hr.employee'].browse(docids)
        birthday_employee = {}
        for rec in employees:
            date_birthday_str = rec.birthday
            if date_birthday_str:
                formatted_date = datetime.strptime(date_birthday_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                birthday_employee[rec.id] = formatted_date
            else:
                birthday_employee[rec.id] = ''
        report_data = {
            'company': self.env.user.company_id,
            "employee": employees,
            'birthday_employee': birthday_employee,


        }

        return report_data
