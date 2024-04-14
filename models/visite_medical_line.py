# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHVisiteMedicalLine(models.Model):
    _name = 'rh.visite.medical.line'

    employee_id = fields.Many2one('hr.employee')
    visite_medical_id = fields.Many2one('rh.visite.medicale')
    date_visite_medicale = fields.Date()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        selected_employees = self.visite_medical_id.visite_medical_lines.mapped('employee_id')
        return {'domain': {'employee_id': [('id', 'not in', selected_employees.ids)]}}
