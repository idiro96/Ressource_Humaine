# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAccidentTravail(models.Model):
    _name = 'rh.accident.travail'

    date_accident_travail = fields.Date()
    description_accident_travail = fields.Char()
    num_pv_accident_travail = fields.Integer()






