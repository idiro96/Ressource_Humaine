# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHEntretien(models.Model):
    _name = 'rh.entretien'

    code_entretien = fields.Char()
    date_entretien = fields.Date()




