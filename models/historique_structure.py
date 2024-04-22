# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_structure(models.Model):
    _name = 'rh.historique.structure'
    _rec_name = 'structure'

    structure = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    date_debut_poste = fields.Date()
    date_fin_poste = fields.Date()
    document_file_line = fields.Binary()
