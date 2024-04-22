# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_fin_relation(models.Model):
    _name = 'rh.historique.fin.relation'
    _rec_name = 'date_fin_relation'

    employee_id = fields.Many2one('hr.employee')
    date_fin_relation = fields.Date()
    document_file_line = fields.Binary()
