# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class RHPlanningLine(models.Model):
    _name = 'rh.planning.line'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _mail_post_access = 'read'

    employee_id = fields.Many2many('hr.employee', tracking=True)
    emphy_id = fields.Many2one('rh.emphy', tracking=True)
    planning_survellance_id = fields.Many2one('rh.planning')
    president_emphy = fields.Many2one('hr.employee', tracking=True)
    date_examen = fields.Date(related="planning_survellance_id.date_surveillance", store=True)
    time_start = fields.Char(related="planning_survellance_id.time_surveillance_start")
    time_end = fields.Char(related="planning_survellance_id.time_surveillance_end")

    # filtered_employee_ids = fields.Many2many('hr.employee', compute='_compute_filtered_employees',
    #                                          string="Filtered Employees")

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        selected_employees = self.planning_survellance_id.planning_surveillance_line.mapped('employee_id')
        return {'domain': {'employee_id': [('id', 'not in', selected_employees.ids)]}}

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

    # @api.model
    # def create(self, vals):
    #     new_record = super(RHPlanningLine, self).create(vals)
    #
    #     message_body = "تحديث قائمة المراقبون:<br/>"
    #     # if 'employee_id' in vals:
    #     #     employee_ids = [int(id) for id in vals.get('employee_id') if isinstance(id, int)]
    #     #     employee_names = self.env['hr.employee'].search([('id', 'in', employee_ids)]).mapped('name')
    #     #     for employee_name in employee_names:
    #     #         message_body += f"  • تعيين الموظف: {employee_name}<br/>"
    #     if 'emphy_id' in vals:
    #         intitule_emphy = self.env['rh.emphy'].browse(vals['emphy_id']).intitule_emphy
    #         message_body += f"  • المدرج: {intitule_emphy}<br/>"
    #     if 'president_emphy' in vals:
    #         president_name = self.env['hr.employee'].browse(vals['president_emphy']).name
    #         message_body += f"  • رئيس المدرج: {president_name}<br/>"
    #
    #     if message_body:
    #         new_record.planning_survellance_id.message_post(body=message_body)
    #
    #     return new_record
    #
    # @api.multi
    # def unlink(self):
    #     for record in self:
    #         message_body = f"قد تم حذف مراقبة المدرج {record.emphy_id.intitule_emphy}"
    #         if message_body:
    #             record.planning_survellance_id.message_post(body=message_body)
    #
    #     return super(RHPlanningLine, self).unlink()
    #
    # def write(self, vals):
    #     # original_employee_id = self.employee_id
    #     original_emphy_id = self.emphy_id
    #     original_president_emphy = self.president_emphy
    #
    #     result = super(RHPlanningLine, self).write(vals)
    #
    #     if any(field in vals for field in
    #            ['emphy_id', 'president_emphy']):
    #         self._track_changes(original_emphy_id, original_president_emphy)
    #
    #     return result
    #
    # def _track_changes(self, original_emphy_id, original_president_emphy):
    #     if self.planning_survellance_id:
    #         new_intitule_emphy = self.emphy_id.intitule_emphy if self.emphy_id else False
    #         old_intitule_emphy = original_emphy_id.intitule_emphy if original_emphy_id else False
    #         new_president_emphy_name = self.president_emphy.name if self.president_emphy else False
    #         old_president_emphy_name = original_president_emphy.name if original_president_emphy else False
    #
    #         message_body = 'تحديث قائمة المراقبون:<br/>'
    #         if old_intitule_emphy != new_intitule_emphy:
    #             if old_intitule_emphy and new_intitule_emphy:
    #                 message_body += f"  • تغيير المدرج من {old_intitule_emphy} إلى {new_intitule_emphy}<br/>"
    #             elif old_intitule_emphy:
    #                 message_body += f"  • حذف المدرج: {old_intitule_emphy}<br/>"
    #             elif new_intitule_emphy:
    #                 message_body += f"  • تعيين المدرج: {new_intitule_emphy}<br/>"
    #
    #         if old_president_emphy_name != new_president_emphy_name:
    #             if old_president_emphy_name and new_president_emphy_name:
    #                 message_body += f"  • تغيير رئيس المدرج {old_president_emphy_name} إلى {new_president_emphy_name}<br/>"
    #             elif old_president_emphy_name:
    #                 message_body += f"  • حذف رئيس المدرج: {old_president_emphy_name}<br/>"
    #             elif new_president_emphy_name:
    #                 message_body += f"  • تعيين رئيس المدرج: {new_president_emphy_name}<br/>"
    #
    #         self.planning_survellance_id.message_post(body=message_body)
