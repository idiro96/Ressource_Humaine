# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHSanction(models.Model):
    _name = 'rh.sanction'

    code_sanction = fields.Char()
    ref_pv_sanction = fields.Char()
    date_pv_sanction = fields.Date()
    num_decision_sanction = fields.Char()
    date_decision_sanction = fields.Date()
