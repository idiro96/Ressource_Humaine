# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistoriqueExterieur(models.Model):
    _name = 'rh.historique.exterieur'
    _rec_name = 'diplôme_ex'

    diplôme_ex = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    document_file_line = fields.Binary()
    type_diplome_ex = fields.Char()
