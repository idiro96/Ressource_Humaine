# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHCommissionPromotion(models.TransientModel):
    _name = 'commission.promotion'


    employee_id_lines = fields.One2many('hr.employee', 'commission_promotion_id', default=lambda self: self._default_employees())



    def valider_commission(self):
        record = self.env['rh.promotion'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            if line.selection_employe == True:
                commission_line = self.env['rh.promotion.commission.line'].create({
                'employee_id': line.id,
                'department_id': line.department_id.name,
                'job_id': line.job_id.name,
                'promotion_id':record.id,
                })


    @api.model
    def _default_employees(self):
        records = self.env['hr.employee'].search([])
        for rec in records:
            rec.selection_employe = False
        return records







