# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_sanction(models.Model):
    _name = 'rh.historique.sanction'
    _rec_name = 'sanction'

    sanction = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    document_file_line = fields.Binary()
