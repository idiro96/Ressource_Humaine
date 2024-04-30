# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrJobInherited(models.Model):
    _inherit = "hr.job"

    # nature_travail_id = fields.Many2one('rh.nature.travail')
    # nature_poste = fields.Selection([('postesuperieure', 'Postesuperieure'),
    #                           ('fonctionsuperieure', 'Fonctionsuperieure'),
    #                           ], readonly=False)
    nature_travail_id = fields.Many2one('rh.type.fonction', track_visibility='onchange')
    poste_organique = fields.Selection(selection=[('organique', 'منصب هيكلي'), ('squelaire', 'منصب عضوي')],
                                       readonly=False, track_visibility='onchange')
    max_employee = fields.Integer(default=1, store=True, track_visibility='onchange')
    nombre_de_postes_vacants = fields.Integer(compute='_compute_nombre_de_postes_vacants', store=True, )
    code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)
    methode_embauche = fields.Selection([('recrutement', 'Recrutement'), ('transfert', 'Transfert'),
                                         ('detachement', 'Detachement'), ], related='employee_ids.methode_embauche')
    name = fields.Char(string='Job Position', required=True, index=True, translate=True, track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(HrJobInherited, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(HrJobInherited, self).write(vals)

    # @api.constrains('no_of_employee', 'max_employee')
    # def _check_max_employee_limit(self):
    #     for job in self:
    #         if job.no_of_employee > job.max_employee:
    #             raise ValidationError("لا يجوز أن عدد الموظفين يتفوق عن الحد الأقصى المسموح به")

    @api.depends('max_employee', 'no_of_employee')
    def _compute_nombre_de_postes_vacants(self):
        for job in self:
            job.nombre_de_postes_vacants = job.max_employee - job.no_of_employee

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(HrJobInherited, self).unlink()


class CustomDepartment(models.Model):
    _inherit = 'hr.department'

    _rec_name = 'name'

    department_type = fields.Selection(selection=[('secretariat', 'Secrétariat'), ('direction', 'Direction'),
                                                  ('service', 'Service'), ('bureau', 'Bureau')], required=True, readonly=False)

    @api.onchange('department_type')
    def onchange_department_type(self):
        domain = []
        if self.department_type == 'direction':
            secretariat_deps = self.env['hr.department'].search([('department_type', '=', 'secretariat')])
            domain += [('id', 'in', secretariat_deps.ids)]
        if self.department_type == 'service':
            direction_deps = self.env['hr.department'].search([('department_type', '=', 'direction')])
            domain += [('id', 'in', direction_deps.ids)]
        if self.department_type == 'bureau':
            service_deps = self.env['hr.department'].search([('department_type', '=', 'service')])
            domain += [('id', 'in', service_deps.ids)]

        return {'domain': {'parent_id': domain}}

    # def _update_employee_manager(self, manager_id):
    #     employees = self.env['hr.employee']
    #     for department in self:
    #         employees = employees | self.env['hr.employee'].search([
    #             ('id', '!=', manager_id),
    #             ('department_id', '=', department.id),
    #             ('parent_id', '=', department.manager_id.id),
    #             ('fin_relation', '=', False)
    #         ])
    #     employees.write({'parent_id': manager_id})
    # employee_id = fields.Many2one('hr.employee')
    # fin_relation = fields.Boolean(related='employee_id.fin_relation')
