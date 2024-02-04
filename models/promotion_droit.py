# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


class RHPromotionDroit(models.Model):
    _name = 'rh.promotion.droit'

    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    job_id = fields.Many2one('hr.job')
    grade_id = fields.Many2one('rh.grade')
    grade_new_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()
    date_new_grade = fields.Date()
    date_promotion = fields.Date()
    duree = fields.Integer()

    sauvegarde = fields.Boolean(Default=False)

    test = fields.Char()

