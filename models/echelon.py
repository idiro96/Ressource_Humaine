# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHEchelon(models.Model):
    _name = 'rh.echelon'
    _rec_name = 'intitule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    intitule = fields.Char(track_visibility='onchange')
    indice_echelon = fields.Integer(track_visibility='onchange')
    categorie_id = fields.Many2one('rh.categorie', track_visibility='onchange')
    groupe_id = fields.Many2one('rh.groupe')
    type_fonction = fields.Many2one('rh.type.fonction',
                                    track_visibility='onchange')
    section = fields.Many2one('rh.section', track_visibility='onchange')
    code_type_fonction = fields.Char(related='type_fonction.code_type_fonction',
                                     string='Code Type Fonction', store=True)
    grille_id = fields.Many2one('rh.grille')
    # description_grille = fields.Char(related='section.categorie_id.grille_id.description_grille', store=True)
    # description_grille2 = fields.Char(related='categorie_id.groupe_id.grille_id.description_grille', store=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')
    grille_compute1_id = fields.Char(compute="_compute_grille")

    @api.multi
    def _compute_grille(self):
        for record in self:
            if record.categorie_id.type_fonction_id.code_type_fonction == 'fonction':
                record.grille_compute1_id = record.categorie_id.groupe_id.grille_id.description_grille
            if record.categorie_id.type_fonction_id.code_type_fonction == 'postesuperieure':
                record.grille_compute1_id = record.categorie_id.groupe_id.grille_id.description_grille
            if record.categorie_id.type_fonction_id.code_type_fonction == 'fonctionsuperieure':
                record.grille_compute1_id = record.categorie_id.grille_id.description_grille
            if record.categorie_id.type_fonction_id.code_type_fonction == 'contractuel':
                record.grille_compute1_id = record.categorie_id.grille_id.description_grille
    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id

        return super(RHEchelon, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHEchelon, self).write(vals)

    @api.depends('categorie_id')
    def _compute_categorie_fields(self):
        for rec in self:
            rec.groupe_id = rec.categorie_id.groupe_id.id if rec.categorie_id else False

    # @api.depends('categorie_id', 'section')
    # def _compute_grille_fields(self):
    #     for rec in self:
    #         if rec.groupe_id:
    #             rec.grille_id = rec.categorie_id.groupe_id.grille_id.id
    #         elif rec.section:
    #             rec.grille_id = rec.section.categorie_id.grille_id.id

    @api.onchange('grille_id')
    def _compute_grille_fields(self):
        for record in self:
            if record.type_fonction.code_type_fonction == 'fonction':
                return {'domain': {
                    'groupe_id': [('grille_id', '=', self.grille_id.id)]}}
            if record.type_fonction.code_type_fonction == 'postesuperieure':
                return {'domain': {
                    'groupe_id': [('grille_id', '=', self.grille_id.id)]}}
            if record.type_fonction.code_type_fonction == 'fonctionsuperieure':
                return {'domain': {
                    'categorie_id': [('grille_id', '=', self.grille_id.id),
                                     ('type_fonction_id', '=', record.type_fonction.id)]}}
            if record.type_fonction.code_type_fonction == 'contractuel':
                return {'domain': {
                    'categorie_id': [('grille_id', '=', self.grille_id.id),
                                     ('type_fonction_id', '=', record.type_fonction.id)]}}
        # for rec in self:
        #     if rec.grille_id:
        #         self.categorie_id = False
        #         type_fonction = self.env['rh.type.fonction'].search([('id', '=', self.type_fonction.id)])
        #         if type_fonction:
        #             return {'domain': {
        #                 'categorie_id': [('grille_id', '=', self.grille_id.id), ('type_fonction_id', '=', type_fonction.id)]}}
        #         else:
        #             return {'domain': {'categorie_id': []}}

    @api.onchange('type_fonction')
    def onchange_type_fonction(self):
        domain = []
        for rec in self:
            if rec.type_fonction:
                categorie = self.env['rh.categorie'].search([('type_fonction_id', '=', rec.type_fonction.id)])
                domain.append(('id', 'in', categorie.ids))
        return {'domain': {'categorie_id': domain}}

    @api.onchange('categorie_id')
    def onchange_categorie_id(self):
        domain = []
        for rec in self:
            if rec.categorie_id:
                section = self.env['rh.section'].search([('categorie_id', '=', rec.categorie_id.id)])
                domain.append(('id', 'in', section.ids))
        return {'domain': {'section': domain}}

    @api.onchange('groupe_id')
    def onchange_groupe_id(self):
        domain = []
        for rec in self:
            return {'domain': {
                    'categorie_id': [('groupe_id', '=', self.groupe_id.id)]}}