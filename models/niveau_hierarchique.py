# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class RHNiveauHierarchique(models.Model):
    _name = 'rh.niveau.hierarchique'
    _rec_name = 'intitule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    bonification_indiciaire = fields.Integer(track_visibility='onchange')
    section_superieure_id = fields.Many2one('rh.section.superieure', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHNiveauHierarchique, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHNiveauHierarchique, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHNiveauHierarchique, self).unlink()
