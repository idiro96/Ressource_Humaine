# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_grade(models.Model):
    _name = 'rh.historique.grade'
    _rec_name = 'grade'

    grade = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    date_debut_travail = fields.Date()
    document_file_line = fields.Binary()
