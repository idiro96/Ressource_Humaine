# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from datetime import datetime


class RHPlanningLine(models.Model):
    _name = 'rh.planning.line'

    # employee_id = fields.Many2many('hr.employee', domain="[('fin_relation', '=', False)] & [('date_debut_conge', '!=', False),('date_debut_conge','>','date_examen')] | [('date_fin_conge', '!=', False),('date_fin_conge','>','date_examen')] ")
    employee_id = fields.Many2many('hr.employee')
                                   # domain="[('fin_relation', '=', False), '|', '&', ('date_debut_conge', '!=', False), ('date_debut_conge', '>', date_examen), '&', ('date_fin_conge', '!=', False), ('date_fin_conge', '>', date_examen)]")
    # employee_id = fields.Many2many('hr.employee',
    #                                domain=[['fin_relation', '=', False], '|', '&', ('fin_relation', '=', False), '|',
    #                                        '&', ('date_debut_conge', '!=', False),
    #                                        ('date_debut_conge', '>', 'date_examen'), '&', ('date_fin_conge', '!=', False),
    #                                        ('date_fin_conge', '>', 'date_examen')])

    # domain = "['&', ['fin_relation', '=', False], '|', '&', ['date_debut_conge', '!=', False], ['date_debut_conge', '>', date_examen], '&', ['date_fin_conge', '!=', False], ['date_fin_conge', '>', date_examen]]"
    # domain = "['|',['fin_relation','=','False'] ,'&', ['fin_relation', '=', False], '|', '&', ['date_debut_conge', '!=', False], ['date_debut_conge', '>', date_examen], '&', ['date_fin_conge', '!=', False], ['date_fin_conge', '>', date_examen]]"

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
        employee = self.env['hr.employee'].search([('fin_relation', '=', False)])

        domain=[]
        for emp in employee:
            print(emp.name)
            conges = self.env['hr.holidays'].search([('employee_id', '=', emp.id)])
            if conges:
                print('lemployee a des conges')
                for conge in conges:
                    print('1er congee de lemployee')
                    date_debut_conge = datetime.strptime(conge.date_from, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    # date_debut_conge=con.date_from.strptime('%y-%m-%d')
                    # print("date_debut_conge")
                    print(date_debut_conge)
                    date_fin_conge = datetime.strptime(conge.date_to, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    # # date_fin_conge=con.date_to.strftime('%y-%m-%d')
                    # print("date_fin_conge")
                    print(date_fin_conge)
                    print("record.date_examen")
                    print(self.planning_survellance_id.date_surveillance)
                    if date_debut_conge > self.planning_survellance_id.date_surveillance or date_fin_conge < self.planning_survellance_id.date_surveillance:
                        print('lemployee libre')
                        # domain.append('|')
                        domain.append(('id', '=', emp.id))
                        break
            else:
                print('lemployee na pas de conges')
                # domain.append('|')
                domain.append(('id', '=', emp.id))

        # variable=self.env['hr.employee'].search(domain)
        print(domain)

        return {'domain': {'employee_id': domain}}
                        # date_debut_conge <= self.date_examen <= date_fin_conge:


    # @api.depends('date_examen')
    # def _compute_filtered_employees(self):
    #     for record in self:
    #         filtered_employees = self.env['hr.employee'].search([])
    #         conges = self.env['hr.holidays'].search([('employee_id', 'in', filtered_employees.ids)])
    #         filtered_employee_ids = []
    #         for employee in filtered_employees:
    #             if employee.fin_relation or any(
    #                     conge.employee_id == employee.id and conge.date_from <= record.date_examen <= conge.date_to
    #                     for conge in conges):
    #                 filtered_employee_ids.append(employee.id)
    #         record.filtered_employee_ids = [(6, 0, filtered_employee_ids)]

    # @api.depends('date_examen')
    # def _compute_filtered_employees(self):
    #     for record in self:
    #         filtered_employee = self.env['hr.employee']
    #         employees = self.env['hr.employee'].search([])
    #         for emp in employees:
    #             conge = self.env['hr.holidays'].search([('employee_id', '=', emp.id)])
    #             if emp.fin_relation or any(con.date_from <= record.date_examen <= con.date_to for con in conge):
    #                 filtered_employee |= emp
    #         record.filtered_employee_ids = filtered_employee
    #
    # employee_ids = fields.Many2many('hr.employee')
    # filtered_employee_ids = fields.Many2many('hr.employee', compute='_compute_filtered_employees')
    #
    # @api.depends('date_examen')
    # def _compute_filtered_employees(self):
    #     for record in self:
    #         filtred_employee=self.env['hr.employee']
    #         employee = self.env['hr.employee'].search([])
    #         for emp in employee:
    #             print(emp.id)
    #             conge = self.env['hr.holidays'].search([('employee_id', '=', emp.id)])
    #             print(conge)
    #             if emp.fin_relation == True:
    #                 print('fin relation true')
    #                 # emp.unlink()
    #                 employee -= emp
    #             elif conge:
    #                 for con in conge:
    #                     date_debut_conge = datetime.strptime(con.date_from, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    #                     # date_debut_conge=con.date_from.strptime('%y-%m-%d')
    #                     print("date_debut_conge")
    #                     print(date_debut_conge)
    #                     date_fin_conge = datetime.strptime(con.date_to, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    #                     # date_fin_conge=con.date_to.strftime('%y-%m-%d')
    #                     print("date_fin_conge")
    #                     print(date_fin_conge)
    #                     print("record.date_examen")
    #                     print(record.date_examen)
    #                     if date_debut_conge <= record.date_examen <= date_fin_conge:
    #                         print("dans if du conge")
    #                         employee -= emp
    #             else:
    #                     print("l'employee n'a pas de conge ni fin de relation")
    #
    #         record.filtered_employee_ids = employee
