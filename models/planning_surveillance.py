# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class RHPlanning(models.Model):
    _name = 'rh.planning'
    _rec_name = 'date_surveillance'
    _order = "date_surveillance desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    date_surveillance = fields.Date(track_visibility='onchange')
    time_surveillance_start = fields.Char(track_visibility='onchange')
    time_surveillance_end = fields.Char(track_visibility='onchange')
    planning_surveillance_line = fields.One2many('rh.planning.line', 'planning_survellance_id', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHPlanning, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHPlanning, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHPlanning, self).unlink()



    @api.constrains('date_surveillance', 'time_surveillance_start', 'time_surveillance_end', 'planning_surveillance_line')
    def _check_employee_availability(self):
        for planning in self:
            for line in planning.planning_surveillance_line:
                conflicting_lines = self.env['rh.planning.line'].search([
                    ('id', '!=', line.id),
                    ('employee_id', 'in', line.employee_id.ids),
                    ('date_examen', '=', planning.date_surveillance),
                    ('time_start', '=', planning.time_surveillance_start),
                    ('time_end', '=', planning.time_surveillance_end),
                ])
                if conflicting_lines:
                    raise ValidationError("لا يجوز للموظف الإشراف على موظفين في نفس الوقت")


    def action_planning(self):
        print()
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'إختيار المراقبون',
            'view_mode': 'form',
            'res_model': 'choisir.planning',
        }



