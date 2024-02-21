from odoo import models, fields, api, _


class PlanningSurveillanceReport(models.AbstractModel):
    _name = 'report.ressource_humaine.notice_planning_surveillance_report'

    @api.model
    def get_report_values(self, docids, data=None):
        planning = self.env['rh.planning'].browse(docids)
        variable = self.env['rh.planning.line'].search("planning_survellance_id", "=", "planning.id")

        planning_surveillance_line = planning.planning_surveillance_line

        # schedule = {}
        # for vari in variable :
        #     for employee in vari.employee_id:
        #         if employee.name not in schedule:
        #             schedule[employee.name] = []
        #             schedule[employee.name].append({
        #                 'date': planning.date_surveillance,
        #                 'start_time': planning.time_surveillance_start,
        #                 'end_time': planning.time_surveillance_end,
        #                 'room': vari.emphy_id.name,
        #             })
        #         elif employee.name in schedule:
        #             if not isinstance(schedule[employee.name]['date'], list):
        #                 schedule[employee.name]['date'] = [schedule[employee.name]['date']]
        #
        #             schedule[employee.name]['date'].append(planning.date_surveillance)
        #
        #             if not isinstance(schedule[employee.name]['start_time'], list):
        #                 schedule[employee.name]['start_time'] = [schedule[employee.name]['start_time']]
        #
        #             schedule[employee.name]['start_time'].append(planning.time_surveillance_start)
        #
        #             if not isinstance(schedule[employee.name]['end_time'], list):
        #                 schedule[employee.name]['end_time'] = [schedule[employee.name]['end_time']]
        #
        #             schedule[employee.name]['end_time'].append(planning.time_surveillance_end)
        #
        #             if not isinstance(schedule[employee.name]['room'], list):
        #                 schedule[employee.name]['room'] = [schedule[employee.name]['room']]
        #
        #             schedule[employee.name]['room'].append(vari.emphy_id.name)
        #




        report_data = {
            # 'employee': employee,
            'planning': planning,
            'variable': variable,
            'company': self.env.user.company_id,
            'planning_surveillance_line': planning_surveillance_line,
            # 'schedule': schedule,
        }

        return report_data
