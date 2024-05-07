# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class RHFiliere(models.Model):
    _name = 'rh.filiere'
    _rec_name = 'intitule_filiere'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    code_group = fields.Char(track_visibility='onchange')
    date_code = fields.Date(track_visibility='onchange')
    intitule_filiere = fields.Char(track_visibility='onchange')
    loi_id = fields.Many2one(comodel_name='rh.loi', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHFiliere, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHFiliere, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHFiliere, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.filiere.sequence') or _('New')
        result = super(RHFiliere, self).create(vals)
        return result
