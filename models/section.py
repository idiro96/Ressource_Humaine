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
    grille_compute1_id = fields.Char(compute="_compute_grille")
    grille_id = fields.Many2one('rh.grille', track_visibility='onchange')
    @api.multi
    def _compute_grille(self):
        for record in self:


            if record.categorie_id.type_fonction_id.code_type_fonction == 'fonctionsuperieure':
                record.grille_compute1_id = record.categorie_id.grille_id.description_grille
            if record.categorie_id.type_fonction_id.code_type_fonction == 'contractuel':
                record.grille_compute1_id = record.categorie_id.grille_id.description_grille

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHSection, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHSection, self).write(vals)

    @api.onchange('grille_id')
    def _onchange_grille_id(self):
        if self.grille_id:
            self.categorie_id = False
            type_fonction = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonctionsuperieure')])
            return {'domain': {'categorie_id': [('grille_id', '=', self.grille_id.id),('type_fonction_id', '=', type_fonction.id)]}}
        else:
            return {'domain': {'categorie_id': []}}

    # @api.onchange('grille_id')
    # def _onchange_grille_id(self):
    #     for rec in self:
    #         domain = []
    #         if self.grille_id:
    #             self.categorie_id = False
    #             type_fonction = self.env['rh.type.fonction'].search([('code_type_fonction ', '=', 'fonctionsuperieure')])
    #             record2 = self.env['rh.categorie'].search(
    #                 [('grille_id', '=', self.grille_id.id), ('type_fonction_id', '=', type_fonction.id)])
    #
    #
    #         return result1
    #
    #         # if self.groupe_id:
    #         type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.nature_travail_id.id)])
    #         print(type_fonction.code_type_fonction)
    #         if type_fonction.code_type_fonction != 'fonctionsuperieure':
    #             if type_fonction.code_type_fonction == 'contractuel':
    #                 return {'domain': {'categorie_new_id': [('grille_id', '=', rec.grille_new_id.id),
    #                                                         (('type_fonction_id', '=',
    #                                                           rec.employee_id.nature_travail_id.id))]}}
    #             elif type_fonction.code_type_fonction != 'contractuel':
    #                 return {'domain': {'groupe_new_id': [('grille_id', '=', rec.grille_new_id.id)]}}
    #         elif type_fonction.code_type_fonction == 'fonctionsuperieure':
    #             print('dfs2')
    #             return {'domain': {'categorie_new_id': [('grille_id', '=', rec.grille_new_id.id),
    #                                                     (('type_fonction_id', '=',
    #                                                       rec.employee_id.nature_travail_id.id))]}}
