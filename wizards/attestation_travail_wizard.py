import re

from datetime import datetime

from odoo import models, fields, api, _


class AttestationTravail(models.TransientModel):
    _name = 'attestation.travail'

    signataire = fields.Selection([('sg', 'الأمانة العامة'), ('dg', 'المدير العام'), ('rl', 'المكلف بالإملاء')], default='sg')
    language = fields.Selection([('ar', 'العربية'), ('fr', 'الفرنسية')], default='ar')
    input = fields.Char(placeholder='مزهوده عبد المليك')

    @api.model
    def _domain_employee_id(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return ['|', ('date_fin_relation', '=', False), ('date_fin_relation', '>', today)]

    employee_id = fields.Many2one('hr.employee', required=True, domain=_domain_employee_id)

    @api.multi
    def print_report(self):
        report_ref = 'ressource_humaine.action_attestation_travail_report'
        if self.language == 'fr':
            report_ref = 'ressource_humaine.action_attestation_travail_fr_report'
        return self.env.ref(report_ref).report_action(self)


class AttestationTravailReport(models.AbstractModel):
    _name = 'report.ressource_humaine.attestation_travail_report'

    @api.model
    def get_report_values(self, docids, data=None):
        attestation_travail = self.env['attestation.travail'].browse(docids[0])

        department_name = attestation_travail.employee_id.department_id.name
        if department_name:
            department_name = re.sub(r'^(مكتب|مصلحة)\s*', '', department_name).strip()

        formatted_date = None
        formatted_date_entrer = None

        if attestation_travail.employee_id.birthday:
            birthday = attestation_travail.employee_id.birthday
            formatted_date = datetime.strptime(birthday, "%Y-%m-%d").strftime("%Y/%m/%d")

        if attestation_travail.employee_id.date_entrer:
            date_entrer = attestation_travail.employee_id.date_entrer
            formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%Y/%m/%d")

        report_data = {
            'department_name': department_name,
            'formatted_date': formatted_date,
            'date_entrer': formatted_date_entrer,
            'attestation_travail': attestation_travail,
            'employee': attestation_travail.employee_id,
            'company': self.env.user.company_id,
        }

        return report_data


class AttestationTravailFrReport(models.AbstractModel):
    _name = 'report.ressource_humaine.attestation_travail_fr_report'

    @api.model
    def get_report_values(self, docids, data=None):
        attestation_travail = self.env['attestation.travail'].browse(docids[0])
        department_name_fr = attestation_travail.employee_id.department_id.intitule
        if department_name_fr:
            department_name_fr = re.sub(r'^(Le Bureau|Le Service|Bureau|Service)\s*', '', department_name_fr).strip()

        formatted_birthday = None
        formatted_date_entrer = None

        if attestation_travail.employee_id.birthday:
            birthday = attestation_travail.employee_id.birthday
            formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%d/%m/%Y")

        if attestation_travail.employee_id.date_entrer:
            date_entrer = attestation_travail.employee_id.date_entrer
            formatted_date_entrer = datetime.strptime(date_entrer, "%Y-%m-%d").strftime("%d/%m/%Y")

        report_data = {
            'department_name_fr': department_name_fr,
            'attestation_travail': attestation_travail,
            'formatted_date_entrer': formatted_date_entrer,
            'formatted_birthday': formatted_birthday,
            'employee': attestation_travail.employee_id,
            'company': self.env.user.company_id,
        }

        return report_data
