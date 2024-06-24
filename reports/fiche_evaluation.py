from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, api, _, fields


class FicheEvaluation(models.AbstractModel):
    _name = 'report.ressource_humaine.fiche_evaluation_report'

    @api.model
    def get_report_values(self, docids, data=None):
        evaluation = self.env['rh.fiche.evaluation'].browse(docids[0])
        fiche_evaluation_lines = self.env['rh.fiche.evaluation.line'].search([('fiche_evaluation_id', '=', evaluation.id)])
        lines_data = []
        for rec in fiche_evaluation_lines:
            date_new_avancement = fields.Date.from_string(rec.fiche_evaluation_id.date_evaluation) if rec.fiche_evaluation_id.date_evaluation else None
            date_old_avancement = fields.Date.from_string(rec.employee_id.date_grade) if rec.employee_id.date_grade else None
            years, months, days = 0, 0, 0
            if date_new_avancement and date_old_avancement:
                delta = relativedelta(date_new_avancement, date_old_avancement)
                years = delta.years
                months = delta.months
                days = delta.days
            time_difference = f"قدرها {years} سنة و {months} شهر و {days} يوم"
            formatted_date_grade = None
            formatted_birthday = None
            if rec.employee_id.date_grade:
                date_grade = rec.employee_id.date_grade
                formatted_date_grade = datetime.strptime(date_grade, "%Y-%m-%d").strftime("%Y/%m/%d")
            if rec.employee_id.birthday:
                birthday = rec.employee_id.birthday
                formatted_birthday = datetime.strptime(birthday, "%Y-%m-%d").strftime("%Y/%m/%d")
            line_data = {
                'nom': rec.employee_id.nom_ar,
                'prenom': rec.employee_id.prenom_ar,
                'grade': rec.employee_id.grade_id.intitule_grade,
                'description': rec.employee_id.grade_id.description,
                'job': rec.employee_id.job_id.name,
                'echelon': rec.employee_id.echelon_id.intitule,
                'note': rec.note,
                'observation': rec.observation,
                'time_difference': time_difference,
                'duree': rec.duree,
                'status': rec.employee_id.marital,
                'gender': rec.employee_id.gender,
                'date_grade': formatted_date_grade,
                'birthday': formatted_birthday,
            }
            lines_data.append(line_data)
        print(lines_data)
        report_data = {
            'evaluation': evaluation,
            'fiche_evaluation_lines': lines_data,
        }
        return report_data
