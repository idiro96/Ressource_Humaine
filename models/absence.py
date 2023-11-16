# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAbsence(models.Model):
    _name = 'rh.absence'

    num_reference_absence = fields.Integer()
    date_debut_absence = fields.Date()
    date_fin_absence = fields.Date()
    nbr_jours_absence = fields.Integer()
    nbre_heure_absence = fields.Integer()
