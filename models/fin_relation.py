# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFinRelation(models.Model):
    _name = 'rh.fin.relation'

    date_fin_relation = fields.Date()
    num_decision_fin_relation = fields.Char()
    type_fin_relation_id = fields.Many2one('rh.type.fin.relation')



