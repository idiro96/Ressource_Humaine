# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class RHPrimeRendementLine(models.Model):
    _name = 'rh.prime.rendement.line'

    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _mail_post_access = 'read'

    prime_rendement_id = fields.Many2one('rh.prime.rendement', tracking=True)
    employee_id = fields.Many2one('hr.employee')
    nbr_jours_travail = fields.Integer(track_visibility='onchange', default=90)
    notation_responsable = fields.Float(track_visibility='onchange', default=30)
    notation_finale = fields.Float(track_visibility='onchange',  compute='_compute_prime_final_fields')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')
    categorie_grade_indice = fields.Integer(related='employee_id.grade_id.categorie_id.Indice_minimal', store=True)

    @api.constrains('notation_responsable')
    def chek_notation(self):
        for rec in self:
            if rec.notation_responsable > 40:
                raise UserError("La notation maximal ne doit pas depasser 40%")


    # @api.model
    # def create(self, vals):
    #     prime = super(RHPrimeRendementLine, self).create(vals)
    #
    #     if float(prime.notation_responsable) > 40:
    #         raise UserError("La notation maximal ne doit pas depasser 40%")
    #     return prime
    @api.depends('nbr_jours_travail','notation_finale')
    def _compute_prime_final_fields(self):
        for rec in self:
            rec.notation_finale = (rec.notation_responsable * rec.nbr_jours_travail) / 90