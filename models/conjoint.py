# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHConjoint(models.Model):
    _name = 'rh.conjoint'
    _rec_name = 'employee_id'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    nom_conjoint = fields.Char(track_visibility='onchange')
    prenom_conjoint = fields.Char(track_visibility="onchange")
    date_naissance_conjoint = fields.Date(track_visibility="onchange")
    lieu_naissance_conjoint = fields.Char(track_visibility="onchange")
    date_mariage = fields.Date(track_visibility="onchange")
    femme_foyer = fields.Boolean(default=False, track_visibility="onchange")
    conjoint_file_lines = fields.One2many('rh.file', 'conjoint_id')
    employee_id = fields.Many2one('hr.employee', track_visibility="onchange")
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHConjoint, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHConjoint, self).write(vals)

