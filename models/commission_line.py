# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHcommissionLine(models.Model):
    _name = 'rh.commission.line'

    employee_id = fields.Many2one('hr.employee')
    sanction_id = fields.Many2one('rh.sanction')
    department_id = fields.Char()
    job_id = fields.Char()
    # date_commission= fields.Date()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        selected_employees = self.sanction_id.employee_id | self.sanction_id.choisir_commission_lines.mapped(
            'employee_id')
        return {'domain': {'employee_id': [('id', 'not in', selected_employees.ids)]}}

