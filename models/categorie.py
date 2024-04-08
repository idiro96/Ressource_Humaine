# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHCategorie(models.Model):
    _name = 'rh.categorie'
    _rec_name = 'intitule'
    _order = "intitule desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    description = fields.Char(track_visibility='onchange')
    Indice_minimal = fields.Integer(track_visibility='onchange')
    groupe_id = fields.Many2one('rh.groupe', track_visibility='onchange')
    grille_id = fields.Many2one('rh.grille', track_visibility='onchange')
    type_fonction_id = fields.Many2one('rh.type.fonction', track_visibility='onchange')
    code_type_fonction = fields.Char(related='type_fonction_id.code_type_fonction', store=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHCategorie, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHCategorie, self).write(vals)

    @api.onchange('grille_id')
    def _onchange_grille_id(self):
        if self.grille_id:
            self.groupe_id = False
            return {'domain': {'groupe_id': [('grille_id', '=', self.grille_id.id)]}}
        else:
            return {'domain': {'groupe_id': []}}
