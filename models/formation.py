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



