# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class HrHolidaysInherited(models.Model):
    _inherit = "hr.holidays"



    def _get_number_of_days(self):

        absence =self.env['rh.absence'].serach()
        res = super(HrHolidaysInherited, self)._get_number_of_days(self, absence.date_debut_absence, absence.date_fin_absence, absence.employee_id)
        """ Returns a float equals to the timedelta between two dates given as string."""
        from_dt = fields.Datetime.from_string(self.date_debut_absence)
        to_dt = fields.Datetime.from_string(self.date_fin_absence)

        if employee_id:
            employee = self.env['hr.employee'].browse(self.employee_id)
            return employee.get_work_days_count(from_dt, to_dt)

        time_delta = to_dt - from_dt
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)
