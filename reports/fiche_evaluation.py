from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, api, _, fields


class FicheEvaluation(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_evaluation_report'

    @api.model
    def get_report_values(self, docids, data=None):
        employee_evaluee = self.env['rh.fiche.evaluation'].browse(docids[0])
        employee_info = self.env['hr.employee'].search([('id', '=', employee_evaluee.employee_id.id)])
        # print(employee_evaluee.grade_id.intitule_grade)

        date_new_avancement = fields.Date.from_string(employee_evaluee.date_evaluation) if employee_evaluee.date_evaluation else None
        date_old_avancement = fields.Date.from_string(employee_info.date_grade) if employee_info.date_grade else None

        years, months, days = 0, 0, 0

        if date_new_avancement and date_old_avancement:
            delta = relativedelta(date_new_avancement, date_old_avancement)
            years = delta.years
            months = delta.months
            days = delta.days

        time_difference = f"قدرها {years} سنة و {months} شهر و {days} يوم"

        formatted_date_grade = None
        formatted_birthday = None

        if employee_info.date_grade:
            date_grade = employee_info.date_grade
            formatted_date_grade = datetime.strptime(date_grade, "%Y-%m-%d").strftime("%Y/%m/%d")

        if employee_info.birthday:
            birthday = employee_info.birthday
            formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%Y/%m/%d")

        report_data = {
            'employee_evaluee': employee_evaluee,
            'employee_info': employee_info,
            'duree': time_difference,
            'date_grade': formatted_date_grade,
            'birthday': formatted_birthday,
        }
        return report_data
