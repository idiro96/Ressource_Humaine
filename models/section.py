# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class RHSection(models.Model):
    _name = 'rh.section'
    _rec_name = 'intitule'

    intitule = fields.Char()
    description = fields.Char()

    categorie_id = fields.Many2one('rh.categorie')
    indice_base = fields.Integer()


