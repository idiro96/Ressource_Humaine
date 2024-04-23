# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHistorique_employee(models.Model):
    _name = 'rh.historique.employee'
    _rec_name = 'grade'

    du = fields.Date()
    au = fields.Date()
    grade = fields.Char()
    poste = fields.Char()
    categorie = fields.Char()
    echelon = fields.Char()
    point_indiciaire = fields.Char()
    structure = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    document_file_line = fields.Binary()
