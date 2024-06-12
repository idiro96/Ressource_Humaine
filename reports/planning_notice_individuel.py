from odoo import models, fields, api, _



class PlanningSurveillanceIndivReport(models.AbstractModel):
    _name = 'report.ressource_humaine.notice_planning_individuel_report'


    @api.model
    def get_report_values(self, docids, data=None):

        employee = self.env['programme.individuel'].browse(docids)
        planning = self.env['hr.employee'].search([('employee_id', '=', employee.employee_id.id)])
        print("planning", planning)


        report_data = {
            'planning': planning,
            "employee": employee,

        }

        return report_data
