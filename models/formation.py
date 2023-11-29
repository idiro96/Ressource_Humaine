# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFormation(models.Model):
    _name = 'rh.formation'

    code_formation = fields.Char()
    intitule_formation = fields.Char()
    date_debut_formation = fields.Date()
    date_fin_formation = fields.Date()
    lieu_formation = fields.Char()
    salle_formation = fields.Char()
    budget_allouee_formation = fields.Float()
    type_formation_id = fields.Many2one('rh.type.formation')
    organisme_id = fields.Many2one('rh.organisme')
    formation_lines = fields.One2many('rh.formation.line', inverse_name='formation_id', string="Formation Lines")
    formation_absence = fields.One2many('rh.absence.formation', inverse_name='formation_id', string="Formation Absence")
    formation_file_lines = fields.One2many('rh.file', 'formation_id')

    def formation_detail_wizard(self):
        return {
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name': 'Formation detail',
        'view_mode': 'form',
        'res_model': 'formation.detail',
        }

