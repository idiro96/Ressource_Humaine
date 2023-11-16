# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFile(models.Model):
    _name = 'rh.file'

    fichier = fields.Binary()
    description_fichier = fields.Date()

