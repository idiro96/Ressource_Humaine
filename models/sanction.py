# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHSanction(models.Model):
    _name = 'rh.sanction'
    _rec_name = 'employee_id'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code_sanction = fields.Char(readonly=True, default=lambda self: _('New'))
    ref_pv_sanction = fields.Char(track_visibility="onchange")
    date_pv_sanction = fields.Date(track_visibility="onchange")
    num_decision_sanction = fields.Char(track_visibility="onchange")
    date_decision_sanction = fields.Date(track_visibility="onchange")
    type_faute_id = fields.Many2one('rh.type.faute', track_visibility="onchange")
    type_sanction_id = fields.Many2one('rh.type.sanction', track_visibility="onchange")
    employee_id = fields.Many2one('hr.employee', track_visibility="onchange")
    choisir_commission_lines = fields.One2many('rh.commission.line', 'sanction_id')
    sanction_file_lines = fields.One2many('rh.file', 'sanction_id')
    state = fields.Selection([('draft', 'Brouillon'),
                              ('confirm', 'Validé'),
                              ('refuse', 'Refusé'), ],
                             readonly=True, default='draft', track_visibility="onchange")
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHSanction, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHSanction, self).write(vals)

    @api.onchange('choisir_commission_lines')
    def _onchange_choisir_commission_lines(self):
        selected_employees = self.choisir_commission_lines.mapped('employee_id')
        return {'domain': {'employee_id': [('id', 'not in', selected_employees.ids)]}}

    def unlink(self):
        for rec in self:
            if rec.state in ['confirm', 'refuse']:
                raise ValidationError('You cannot delete a record that is confirmed or refused.')
        return super(RHSanction, self).unlink()

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'refuse'

    @api.model
    def create(self, vals):
        if vals.get('code_sanction', _('New')) == _('New'):
            vals['code_sanction'] = self.env['ir.sequence'].next_by_code('rh.sanction.sequence') or _('New')
        result = super(RHSanction, self).create(vals)
        return result

    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'إختيار اللجنة',
            'view_mode': 'form',
            'res_model': 'choisir.commission',
        }
