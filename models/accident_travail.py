# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class RHAccidentTravail(models.Model):
    _name = 'rh.accident.travail'
    _rec_name = 'employee_id'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    date_accident_travail = fields.Date(track_visibility='onchange')
    description_accident_travail = fields.Text(track_visibility='onchange')
    num_pv_accident_travail = fields.Integer(track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', track_visibility='onchange')
    accident_travail_file_lines = fields.One2many('rh.file', 'accident_travail_id')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHAccidentTravail, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHAccidentTravail, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHAccidentTravail, self).unlink()






