# -*- coding: utf-8 -*-
import math

import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_diplome(models.Model):
    _name = 'rh.historique.diplome'
    _rec_name = 'diplôme'

    diplôme = fields.Char()
    document_file_line_filename = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    document_file_line = fields.Binary()
    type_diplome = fields.Selection(
        [('enseignementsuperieure', 'Enseignement supérieure'), ('secondaire', 'Secondaire'),('moyen', 'Moyen'),('primaire', 'Primaire'), ('formationprofessionnel', 'Formation Professionnelle'),
         ('formationameliorerniveau', 'Formation et amélioration niveau')])





