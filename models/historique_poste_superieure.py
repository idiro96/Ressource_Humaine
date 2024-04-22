# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_poste_superieure(models.Model):
    _name = 'rh.historique.poste.superieure'
    _rec_name = 'type_poste'

    type_poste = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    date_debut_poste = fields.Date()
    date_fin_poste = fields.Date()
    document_file_line = fields.Binary()
