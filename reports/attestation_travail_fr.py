import re

from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeAttestationTravailFr(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_employee_attestation_travail_fr_report').report_action(self)


class EmployeeAttestationTravailFrReport(models.AbstractModel):
    _name = 'report.ressource_humaine.employee_attestation_travail_fr_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].browse(docids[0])
        department_name_fr = employee.department_id.intitule
        if department_name_fr:
            department_name_fr = re.sub(r'^(Le Bureau|Le Service|Bureau|Service)\s*', '', department_name_fr).strip()

        formatted_date_entrer = None
        formatted_birthday = None

        if employee.birthday:
            birthday = employee.birthday
            formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%d/%m/%Y")
        if employee.date_entrer:
            date_entrer = employee.date_entrer
            formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%d/%m/%Y")

        report_data = {
            'department_name_fr': department_name_fr,
            'formatted_date_entrer': formatted_date_entrer,
            'formatted_birthday': formatted_birthday,
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data
