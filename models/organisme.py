# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHOrganisme(models.Model):
    _name = 'rh.organisme'
    _rec_name = 'rs_organisme'
    _order = "rs_organisme"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code_organisme = fields.Char()
    rs_organisme = fields.Char(track_visibility='onchange')
    adresse_organisme = fields.Char(track_visibility='onchange')
    organisme_file_lines = fields.One2many('rh.file', 'organisme_id')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHOrganisme, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHOrganisme, self).write(vals)
