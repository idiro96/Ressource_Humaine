# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from werkzeug.routing import ValidationError


class RHDecisionCorpsLine(models.Model):
    _name = 'rh.corps.decision.line'
    # _rec_name = 'intitule_grade'
    # _order = "intitule_grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char()
    date = fields.Date()
    date_debut = fields.Date()
    corps_id = fields.Many2one('rh.corps', track_visibility='onchange')


