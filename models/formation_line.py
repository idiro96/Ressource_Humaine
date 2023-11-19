# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFormationLine(models.Model):
    _name = 'rh.formation.line'

    employee_id = fields.Many2one('hr.employee')
    formation_id = fields.Many2one('rh.formation')
    nbr_jour_assiste = fields.Integer()









