# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.addons.hr_holidays.models.hr_holidays import Holidays

from odoo.exceptions import ValidationError


class HrHolidaysInherited(models.Model):
    _inherit = "hr.holidays"

    @api.multi
    def print_conge(self):
        return self.env.ref('ressource_humaine.report_titre_conge').report_action(self)

    @api.multi
    def note_conge(self):
        return self.env.ref('ressource_humaine.report_note_conge').report_action(self)

    @api.multi
    def planning_conge(self):
        return self.env.ref('ressource_humaine.report_planning_conge').report_action(self)

    @api.multi
    def _check_holidays(self):
        # Votre code ici
        leave_days = 0

        employ = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        if employ:
            leave_days = employ.days_off
            leave_days = 0
            print('ici conge1')
        result = super(Holidays, self)._check_holidays()
        employ.write({'days_off': 0})
        print('ici conge2')
        # Votre code supplémentaire ici
        return result
    @api.model
    def create(self, vals):
        holidays = super(HrHolidaysInherited, self).create(vals)
        employ = self.env['hr.employee'].search([('id', '=', holidays.employee_id.id)])
        if employ:
                print('rrrrrrr')
                if employ.days_off >= holidays.number_of_days_temp:
                    droitconge  = self.env['rh.congedroit'].search([('id_personnel', '=',employ.id)])
                    jours_conge = holidays.number_of_days_temp
                    nbr_jour_reste = 0
                    nbr_jour_consomme = 0
                    for droit in droitconge:
                        if droit.nbr_jour >= droit.nbr_jour_reste:
                            if droit.nbr_jour_reste > jours_conge:
                                if jours_conge > 0:
                                    nbr_jour_reste = droit.nbr_jour_reste - jours_conge
                                    nbr_jour_consomme = droit.nbr_jour - nbr_jour_reste
                                    jours_conge = holidays.number_of_days_temp - jours_conge
                                    droit.write({'nbr_jour_reste': nbr_jour_reste})
                                    droit.write({'nbr_jour_consomme': nbr_jour_consomme})
                            else:
                                droit.nbr_jour_reste = 0
                                nbr_jour_consomme = droit.nbr_jour - nbr_jour_reste
                                # jours_conge = 0
                                droit.write({'nbr_jour_reste': 0})
                                droit.write({'nbr_jour_consomme': nbr_jour_consomme})

                    leave_days = employ.days_off-holidays.number_of_days_temp
                    employ.write({'days_off': leave_days})
                    print(leave_days)
                    print(employ.days_off)
                else:
                    raise ValidationError(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                            'Please verify also the leaves waiting for validation.'))

        print('rrrrrrr2')

        return holidays
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





    # @api.model
    # def _compute_days_off_scheduler(self):
    #     records = self.search([])  # Fetch all records of your model
    #     for record in records:
    #         current_date = fields.Date.today()
    #         last_updated_date = record.last_updated_date
    #
    #         if last_updated_date:
    #             months_passed = (current_date.year - last_updated_date.year) * 12 + current_date.month - last_updated_date.month
    #             days_increment = months_passed * 2.5
    #             record.days_off += days_increment
    #             record.last_updated_date = current_date
    #
    # def schedule_compute_days_off(self):
    #     # Create a scheduler to call the computation method every month
    #     next_call = datetime.now() + timedelta(days=30)  # Set the interval for 30 days
    #     self.env['ir.cron'].sudo().create({
    #         'name': 'Compute Days Off Scheduler',
    #         'model_id': self.env.ref('your_module_name.model_your_model_name').id,  # Replace with your model's reference
    #         'state': 'code',
    #         'code': 'model.schedule_compute_days_off()',
    #         'interval_number': 1,
    #         'interval_type': 'months',
    #         'numbercall': -1,
    #         'nextcall': next_call.strftime('%Y-%m-%d %H:%M:%S'),
    #         'user_id': self.env.user.id,
    #     })



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
