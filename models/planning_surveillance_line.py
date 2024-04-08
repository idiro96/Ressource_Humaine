# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class RHPlanningLine(models.Model):
    _name = 'rh.planning.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    employee_id = fields.Many2many('hr.employee', track_visibility='onchange')
    emphy_id = fields.Many2one('rh.emphy', track_visibility='onchange')
    planning_survellance_id = fields.Many2one('rh.planning')
    president_emphy = fields.Many2one('hr.employee', track_visibility='onchange')
    date_examen = fields.Date(related="planning_survellance_id.date_surveillance", store=True)
    time_start = fields.Char(related="planning_survellance_id.time_surveillance_start")
    time_end = fields.Char(related="planning_survellance_id.time_surveillance_end")

    filtered_employee_ids = fields.Many2many('hr.employee', compute='_compute_filtered_employees',
                                             string="Filtered Employees")

    @api.onchange('date_examen')
    def onchange_date(self):
        domain = []
        for emp in self.env['hr.employee'].search([]):
            if emp.fin_relation or emp.position_statutaire != 'activite':
                domain.append(emp.id)
            else:
                conges = self.env['hr.holidays'].search([('employee_id', '=', emp.id), ('state', '=', 'validate')])
                if conges:
                    for conge in conges:
                        date_debut_conge = datetime.strptime(conge.date_from, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                        date_fin_conge = datetime.strptime(conge.date_to, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                        if date_debut_conge < self.planning_survellance_id.date_surveillance < date_fin_conge:
                            domain.append(emp.id)
                            break
            # sanction = self.env['rh.sanction'].search([('employee_id', '=', emp.id), ('state', '=', 'confirm')])
            # formations = self.env['rh.formation.line'].search([('employee_id', '=', emp.id)])

            # if sanction:
            #     date_sanction = sanction.date_decision_sanction
            #     if date_sanction < self.planning_survellance_id.date_surveillance:
            #         print('sanction')
            #         print(emp.name)
            #         domain.append(emp.id)

            # if formations:
            #     for formation in formations:
            #         debut = formation.date_debut_formation_line
            #         fin = formation.date_fin_formation_line
            #         if debut < self.planning_survellance_id.date_surveillance and fin > self.planning_survellance_id.date_surveillance:
            #             print('formation')
            #             print(emp.name)
            #             domain.append(emp.id)
            #             break

        return {'domain': {'employee_id': [('id', 'not in', domain)]}}
