from odoo import models, fields, api, _


class ListeDesEmployes(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_employee'

    @api.model
    def get_report_values(self, docids, data=None):

        def custom_sort_key(employee):
            job_name = employee.job_id.name or ''
            if 'مدير عام' in job_name:
                return (0, job_name)
            elif 'الأمين العام' in job_name:
                return (1, job_name)
            elif 'مدير' in job_name:
                return (2, job_name)
            elif 'رئيس مصلحة' in job_name:
                return (3, job_name)
            elif 'رئيس مكتب' in job_name:
                return (4, job_name)
            elif 'رئيس' in job_name:
                return (5, job_name)
            elif 'مسؤول' in job_name:
                return (6, job_name)
            else:
                return (7, job_name)


        employees = self.env['hr.employee'].search([('fin_relation', '=', False)],
                                                   order='categorie_grade_indice desc, grade_id')


        employee = sorted(employees, key=custom_sort_key)
        print('hadjiiiiiiiiiiiiiiiiii')
        print(employee)


        report_data = {
            'employee': employee,
            'company': self.env.user.company_id,
        }

        return report_data

