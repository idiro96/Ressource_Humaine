# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHEnfant(models.Model):
    _name = 'rh.enfant'


    nom_enfant = fields.Char()
    prenom_enfant = fields.Char()
    date_naissance_enfant = fields.Date()
    scolarite = fields.Boolean(default=False)