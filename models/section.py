# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHSection(models.Model):
    _name = 'rh.section'
    _rec_name = 'intitule'
    _order = "intitule"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    description = fields.Char(track_visibility='onchange')
    categorie_id = fields.Many2one('rh.categorie', domain="[('type_fonction_id', 'in', ['منصب عالي', 'وظيفة عليا'])]", track_visibility='onchange')
    indice_base = fields.Integer(track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHSection, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHSection, self).write(vals)
