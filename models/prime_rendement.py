# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class RHPrimeRendement(models.Model):
    _name = 'rh.prime.rendement'
    _order = "date_debut desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'


    date_debut = fields.Date(track_visibility='onchange')
    date_fin = fields.Date(track_visibility='onchange')
    exercice = fields.Char(track_visibility='onchange', compute='_compute_exercice_fields')
    prime_rendement_lines = fields.One2many('rh.prime.rendement.line', 'prime_rendement_id',
                                                 track_visibility='onchange')

    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')


    def _compute_exercice_fields(self):
        for rec in self:
            if rec.date_fin:
                date_obj = fields.Date.from_string(rec.date_fin)
                rec.exercice = date_obj.year