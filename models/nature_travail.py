# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHNaturetravail(models.Model):
    _name = 'rh.nature.travail'
    _rec_name = 'intitule'

    code = fields.Char()
    intitule = fields.Char()
    nbr_poste_max = fields.Integer()
    nbr_poste_existe = fields.Integer()
    nbr_poste_non_occupe = fields.Integer()

