# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHCabinetMedical(models.Model):
    _name = 'rh.cabinet.medical'
    _rec_name = 'raison_social'
    _order = "raison_social"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    raison_social = fields.Char(track_visibility='onchange')
    nif_cabinet = fields.Char(track_visibility='onchange')
    nis_cabinet = fields.Char(track_visibility='onchange')
    num_article = fields.Char(track_visibility='onchange')
    adress = fields.Char(track_visibility='onchange')
    contact = fields.Char(track_visibility='onchange')
    rc = fields.Char(track_visibility='onchange')
    cabinet_medicale_file_lines = fields.One2many('rh.file', 'cabinet_medicale_id')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHCabinetMedical, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHCabinetMedical, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.cabinet.medical.sequence') or _('New')
        result = super(RHCabinetMedical, self).create(vals)
        return result
