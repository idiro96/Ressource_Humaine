# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from werkzeug.routing import ValidationError


class RHGradeLine(models.Model):
    _name = 'rh.grade.line'
    # _rec_name = 'intitule_grade'
    # _order = "intitule_grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # code = fields.Char(readonly=True)
    # intitule_grade = fields.Char(required=True)
    grade_id = fields.Many2one(comodel_name='rh.grade', track_visibility="onchange")
    grade2_id = fields.Many2one(comodel_name='rh.grade', track_visibility="onchange")

