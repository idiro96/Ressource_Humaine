# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_position_statutaire(models.Model):
    _name = 'rh.historique.position.statutaire'
    _rec_name = 'position_statutaire'

    position_statutaire = fields.Selection([('activite', 'Activite'),
                                            ('detachement', 'Detachement'),
                                            ('horscadre', 'Horscadre'), ('miseendisponibilite', 'Miseendisponibilite'),
                                            ('servicenationale', 'Servicenationale')],
                                           readonly=False, default='activite')

    employee_id = fields.Many2one('hr.employee')
    date_debut_poste = fields.Date()
    date_fin_poste = fields.Date()
    document_file_line = fields.Binary()
