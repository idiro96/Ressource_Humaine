# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHCategorie(models.Model):
    _name = 'rh.categorie'
    _rec_name = 'intitule'

    intitule = fields.Char()
    description = fields.Char()
    Indice_minimal = fields.Integer()
    groupe_id = fields.Many2one('rh.groupe')
    grille_id = fields.Many2one('rh.grille')
    type_fonction_id = fields.Many2one('rh.type.fonction')
