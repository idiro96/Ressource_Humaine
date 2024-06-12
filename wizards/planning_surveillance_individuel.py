from odoo import models, fields, api, _
import datetime
import babel.dates


class ProgrammeIndividuel(models.TransientModel):

    _name = 'programme.individuel'


    employee_id = fields.Many2one('hr.employee')
    lieu_examen = fields.Text()
    date_examanen = fields.Datetime()
    formatted_date_examanen = fields.Char(compute='_compute_formatted_date_examanen', store=True)
    place_examen = fields.Text()


    @api.depends('date_examanen')
    def _compute_formatted_date_examanen(self):
        for record in self:
            if record.date_examanen:
                date_dt = fields.Datetime.from_string(record.date_examanen)
                user_lang = self.env.user.lang or 'ar'

                # Format date
                formatted_date = date_dt.strftime('%Y/%m/%d')

                # Format time
                formatted_time = date_dt.strftime('%I:%M %p')

                # Get Arabic day name
                arabic_day = babel.dates.format_date(date_dt, 'EEEE', locale=user_lang)

                # Translate AM/PM to Arabic
                arabic_time_period = 'صباحا' if 'AM' in formatted_time else 'مساء'
                arabic_time = formatted_time.split(' ')[0]

                # Compose the final string
                record.formatted_date_examanen = f"يوم {arabic_day} {formatted_date} على الساعة {arabic_time} {arabic_time_period}"
            else:
                record.formatted_date_examanen = ''

    def print_report(self):
        # Ensure the formatted date is computed
        self._compute_formatted_date_examanen()
        return self.env.ref('ressource_humaine.action_notice_planning_individuel_report').report_action(self)