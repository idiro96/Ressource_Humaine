# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHConge(models.Model):
    _name = 'rh.conge'

    exercice_conge = fields.Char()
    nbr_jour = fields.Integer()
    nbr_jour_consomme = fields.Integer()
    nbr_jour_reste = fields.Integer()




