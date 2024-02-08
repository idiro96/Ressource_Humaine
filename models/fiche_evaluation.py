# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'

    date_evaluation = fields.Date()
    employee_id = fields.Many2one('hr.employee')
    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    echelon_id = fields.Many2one('rh.echelon')
    date_grade = fields.Date()
    note = fields.Integer()
    observation = fields.Char()


