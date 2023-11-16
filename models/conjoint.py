# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHConjoint(models.Model):
    _name = 'rh.conjoint'


    nom_conjoint = fields.Char()
    prenom_conjoint = fields.Char()
    date_naissance_conjoint = fields.Date()
    lieu_naissance_conjoint = fields.Char()
    date_mariage = fields.Date()
    femme_foyer = fields.Boolean(default=False)


