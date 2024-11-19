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
                print("rabahhhhhhhhh")
                print(date_birthday_str)
                formatted_date = datetime.strptime(date_birthday_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                birthday_employee[rec.id] = formatted_date
                print("rabahhhhhhhhh")
                print(birthday_employee)
            else:
                birthday_employee[rec.id] = ''

        date_debut_emploi_employee = {}
        for rec in employees:
            date_debut_emploi_str = rec.date_debut_emploi
            if date_birthday_str:
                formatted_date = datetime.strptime(date_debut_emploi_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                date_debut_emploi_employee[rec.id] = formatted_date

            else:
                date_debut_emploi_employee[rec.id] = ''

        date_entrer_employee = {}
        for rec in employees:
            date_entrer_str = rec.date_entrer
            if date_entrer_str:
                formatted_date = datetime.strptime(date_entrer_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                date_entrer_employee[rec.id] = formatted_date

            else:
                date_entrer_employee[rec.id] = ''

            date_grade_employee = {}
            for rec in employees:
                date_grade_str = rec.date_grade
                if date_grade_str:
                    formatted_date = datetime.strptime(date_grade_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                    date_grade_employee[rec.id] = formatted_date

                else:
                    date_grade_employee[rec.id] = ''
        report_data = {
            'company': self.env.user.company_id,
            "employee": employees,
            'birthday_employee': birthday_employee,
            'date_debut_emploi_employee': date_debut_emploi_employee,
            'date_entrer_employee': date_entrer_employee,
            'date_grade_employee': date_grade_employee,


        }

        return report_data
