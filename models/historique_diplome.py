# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_diplome(models.Model):
    _name = 'rh.historique.diplome'
    _rec_name = 'diplôme'

    diplôme = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    document_file_line = fields.Binary()
    type_diplome = fields.Selection(
        [('enseignementsuperieure', 'Enseignement supérieure'), ('secondaire', 'Secondaire'), ('formationprofessionnel', 'Formation Professionnelle')]
  )