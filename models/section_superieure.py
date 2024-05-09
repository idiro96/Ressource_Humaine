# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class RHSectionSuperieure(models.Model):
    _name = 'rh.section.superieure'
    _rec_name = 'intitule'
    _order = "intitule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    description = fields.Char(track_visibility='onchange')
    categorie_superieure_id = fields.Many2one('rh.categorie.superieure', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHSectionSuperieure, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHSectionSuperieure, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHSectionSuperieure, self).unlink()
