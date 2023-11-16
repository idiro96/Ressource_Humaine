# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHContrat(models.Model):
    _name = 'rh.contrat'

    code_contrat = fields.Char()
    date_debut_contrat = fields.Date()
    date_fin_contrat = fields.Date()
    salaire_base_contrat = fields.Float()
    motif_contrat = fields.Char()
    type_contrat_id = fields.Many2one('rh.type.contrat')



