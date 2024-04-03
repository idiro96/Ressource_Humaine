# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class RHPlanningLine(models.Model):
    _name = 'rh.planning.line'

    employee_id = fields.Many2many('hr.employee')
    emphy_id = fields.Many2one('rh.emphy')
    planning_survellance_id = fields.Many2one('rh.planning')
    president_emphy = fields.Many2one('hr.employee')
    date_examen = fields.Date(related="planning_survellance_id.date_surveillance", store=True)
    time_start = fields.Char(related="planning_survellance_id.time_surveillance_start")
    time_end = fields.Char(related="planning_survellance_id.time_surveillance_end")

    filtered_employee_ids = fields.Many2many('hr.employee', compute='_compute_filtered_employees',
                                             string="Filtered Employees")




    @api.onchange('date_examen')
    def onchange_date(self):
        domain = []
        for emp in self.env['hr.employee'].search([('fin_relation', '=', False)]):
            conges = self.env['hr.holidays'].search([('employee_id', '=', emp.id), ('state', '=', 'validate')])
            sanction = self.env['rh.sanction'].search([('employee_id', '=', emp.id)])
            if conges:
                for conge in conges:
                    date_debut_conge = datetime.strptime(conge.date_from, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    date_fin_conge = datetime.strptime(conge.date_to, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    if date_debut_conge > self.planning_survellance_id.date_surveillance or date_fin_conge < self.planning_survellance_id.date_surveillance:
                        if not sanction:
                            domain.append(emp.id)
                            break
            elif sanction:
                date_sanction = datetime.strptime(sanction.date_decision_sanction, "%Y-%m-%d").strftime("%Y-%m-%d")
                if date_sanction > self.planning_survellance_id.date_surveillance:
                    domain.append(emp.id)
            else:
                domain.append(emp.id)

        return {'domain': {'employee_id': [('id', 'in', domain)]}}
