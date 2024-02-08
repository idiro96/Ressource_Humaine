# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'

    date_evaluation = fields.Date()
    employee_id = fields.Many2one('hr.employee')
    grade_id = fields.Many2one('rh.grade',compute='_onchange_employee_id', store=True)
    job_id = fields.Many2one('hr.job',compute='_onchange_employee_id', store=True)
    echelon_id = fields.Many2one('rh.echelon',compute='_onchange_employee_id', store=True)
    date_grade = fields.Date()
    note = fields.Integer()
    observation = fields.Char()
    fiche_evaluation_file = fields.Binary()

    # @api.model
    # def create(self, vals):
    #     evalutation = super(RHFicheEvaluation, self).create(vals)
    #     for rec in self:
    #         vals['grade_id'] = evalutation.employee_id.grade_id
    #         vals['job_id'] = evalutation.employee_id.job_id
    #         vals['echelon_id'] = evalutation.employee_id.echelon_id
    #     return evalutation

    @api.depends('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            rec.grade_id = rec.employee_id.grade_id
            rec.job_id = rec.employee_id.job_id
            rec.echelon_id = rec.employee_id.echelon_id



