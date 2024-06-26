# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHAbsence(models.Model):
    _name = 'rh.absence'
    _rec_name = 'employee_id'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    num_reference_absence = fields.Integer()
    date_debut_absence = fields.Datetime(track_visibility="onchange")
    date_fin_absence = fields.Datetime(track_visibility="onchange")
    nbr_jours_absence = fields.Integer(track_visibility="onchange")
    nbre_heure_absence = fields.Float(track_visibility="onchange")
    employee_id = fields.Many2one('hr.employee', track_visibility="onchange")
    type_absence_id = fields.Many2one('rh.type.absence', track_visibility="onchange")
    absence_file_lines = fields.One2many('rh.file', 'absence_id')
    state = fields.Selection([('draft', 'Brouillon'), ('confirm', 'Validé'), ('refuse', 'Refusé')], readonly=True,
                             default='draft', track_visibility="onchange")
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHAbsence, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHAbsence, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.state in ['confirm', 'refuse']:
                raise ValidationError('You cannot delete a record that is confirmed or refused.')
        return super(RHAbsence, self).unlink()

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'refuse'

    @api.constrains('date_debut_absence', 'date_fin_absence', 'employee_id')
    def _check_contract_overlap(self):
        for absence in self:
            overlapping_absence = self.search([
                ('employee_id', '=', absence.employee_id.id),
                ('date_debut_absence', '<=', absence.date_fin_absence),
                ('date_fin_absence', '>=', absence.date_debut_absence),
                ('id', '!=', absence.id),
            ])
            if overlapping_absence:
                raise ValidationError("cette employé posséde une absence dans cette période")

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)

        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee.get_work_days_count(from_dt, to_dt)

        time_delta = to_dt - from_dt
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)

    @api.onchange('date_fin_absence')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        date_from = self.date_debut_absence
        date_to = self.date_fin_absence

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.nbr_jours_absence = self._get_number_of_days(date_from, date_to, self.employee_id.id)

        else:
            self.nbr_jours_absence = 0
