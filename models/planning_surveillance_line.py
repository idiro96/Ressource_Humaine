# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _




class RHPlanningLine(models.Model):
    _name = 'rh.planning.line'

    employee_id = fields.Many2many('hr.employee')
    emphy_id = fields.Many2one('rh.emphy')
    planning_survellance_id = fields.Many2one('rh.planning')
    president_emphy = fields.Many2one('hr.employee')
    time_surveillance_start = fields.Char()
    time_surveillance_end = fields.Char()
