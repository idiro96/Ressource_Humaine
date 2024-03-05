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
    nature_travail_id = fields.Many2one('rh.type.fonction')
    poste_organique = fields.Selection(selection=[('organique', 'منصب هيكلي'), ('squelaire', 'منصب عضوي')],
                                       readonly=False)
    max_employee = fields.Integer(default=1, store=True)
    nombre_de_postes_vacants = fields.Integer(compute='_compute_nombre_de_postes_vacants', store=True, )
    code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)

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
            "Vous ne pouvez pas supprimer cet enregistrement")
        return super(HrJobInherited, self).unlink()

    @api.depends('no_of_recruitment', 'employee_ids.job_id', 'employee_ids.active', 'employee_ids.methode_embauche')
    def _compute_employees(self):
        for job in self:
            if job.employee_ids.methode_embauche == 'recrutement':
                employee_data = self.env['hr.employee'].read_group([('job_id', 'in', job.ids)], ['job_id'], ['job_id'])
                result = dict((data['job_id'][0], data['job_id_count']) for data in employee_data)
                job.no_of_employee = result.get(job.id, 0)
                job.expected_employees = result.get(job.id, 0) + job.no_of_recruitment
