# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class RHGroupe(models.Model):
    _name = 'rh.groupe'
    _rec_name = 'name'
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    name = fields.Char(track_visibility='onchange')
    description = fields.Char(track_visibility='onchange')
    grade_lines = fields.One2many('rh.grade', inverse_name='grade_id')
    grille_id = fields.Many2one('rh.grille', track_visibility='onchange')
    categorie_lines = fields.One2many('rh.categorie', inverse_name='groupe_id', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHGroupe, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHGroupe, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHGroupe, self).unlink()

