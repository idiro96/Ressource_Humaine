# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHPromotion(models.Model):
    _name = 'rh.promotion'

    date_examin_professionnel = fields.Date()
    code = fields.Char()
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='promotion_id')
    promotion_file_lines = fields.One2many('rh.file', 'promotion_id')




