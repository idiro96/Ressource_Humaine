# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class RHPlanning(models.Model):
    _name = 'rh.planning'
    _rec_name = 'date_surveillance'

    date_surveillance = fields.Date()
    time_surveillance_start = fields.Char()
    time_surveillance_end = fields.Char()
    planning_surveillance_line = fields.One2many('rh.planning.line', 'planning_survellance_id')

    @api.constrains('date_surveillance', 'time_surveillance_start', 'time_surveillance_end', 'planning_surveillance_line')
    def _check_employee_availability(self):
        for planning in self:
            for line in planning.planning_surveillance_line:
                conflicting_lines = self.env['rh.planning.line'].search([
                    ('id', '!=', line.id),
                    ('employee_id', 'in', line.employee_id.ids),
                    ('date_examen', '=', planning.date_surveillance),
                    ('time_start', '=', planning.time_surveillance_start),
                    ('time_end', '=', planning.time_surveillance_end),
                ])
                if conflicting_lines:
                    raise ValidationError("un employee ne peut pas surveiller deux emphy au meme horraire")


    def action_planning(self):
        print()
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'إختيار المراقبون',
            'view_mode': 'form',
            'res_model': 'choisir.planning',
        }



