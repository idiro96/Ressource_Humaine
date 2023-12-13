# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _



class HrHolidaysInherited(models.Model):
    _inherit = "hr.holidays"


    # def job(self):
    #     print("Executing the cron job0!")
    #
    # # Define the schedule (e.g., every minute)
    # schedule.every(1).minutes.do(job)
    #
    # # Run the scheduler
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)




    # def _get_number_of_days(self):
    #
    #    print('test')

    # def _get_number_of_days(self):
    #

    #     absence =self.env['rh.absence'].serach()
    #     res = super(HrHolidaysInherited, self)._get_number_of_days(self, absence.date_debut_absence, absence.date_fin_absence, absence.employee_id)
    #     """ Returns a float equals to the timedelta between two dates given as string."""
    #     from_dt = fields.Datetime.from_string(self.date_debut_absence)
    #     to_dt = fields.Datetime.from_string(self.date_fin_absence)
    #
    #     if self.employee_id:
    #         employee = self.env['hr.employee'].browse(self.employee_id)
    #         return employee.get_work_days_count(from_dt, to_dt)
    #
    #     time_delta = to_dt - from_dt
    #     return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)
