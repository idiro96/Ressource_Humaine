# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHCongeDroit(models.Model):
    _name = 'rh.congedroit'


    id_personnel = fields.Many2one(comodel_name='hr.holidays')
    exercice_conge = fields.Char()
    nbr_jour = fields.Float()
    nbr_jour_consomme = fields.Float()
    nbr_jour_reste = fields.Float()




