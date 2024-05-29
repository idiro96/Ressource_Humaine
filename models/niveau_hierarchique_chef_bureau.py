# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class RHNiveauHierarchiqueCheBureau(models.Model):
    _name = 'rh.niveau.hierarchique.chef.bureau'
    _rec_name = 'intitule'
    _order = "grille_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    bonification_indiciaire = fields.Integer(track_visibility='onchange')
    grille_id = fields.Many2one('rh.grille', readonly=False, track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')
    old_chef_bureau_id = fields.Many2one('rh.niveau.hierarchique.chef.bureau', track_visibility='onchange')
    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHNiveauHierarchiqueCheBureau, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHNiveauHierarchiqueCheBureau, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHNiveauHierarchiqueCheBureau, self).unlink()
