# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _


class RHPlanning(models.Model):
    _name = 'rh.planning'
    _rec_name = 'president_emphy'


    date_surveillance = fields.Date()
    president_emphy = fields.Many2one('hr.employee')
    time_surveillance_start = fields.Datetime(widget='datetime')
    time_surveillance_end = fields.Float(widget='time')
    # time_surveillance_end1 = fields.Datetime()
    planning_surveillance_line = fields.One2many('rh.planning.line', 'planning_survellance_id')


    def action_planning(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'إختيار المراقبون',
            'view_mode': 'form',
            'res_model': 'choisir.planning',
        }



