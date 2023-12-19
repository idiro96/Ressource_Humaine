# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHLoi(models.Model):
    _name = 'rh.loi'

    code = fields.Char(String='Code', readonly=True, default=lambda self: _('New'))
    intitule_loi = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.loi.sequence') or _('New')
        result = super(RHLoi, self).create(vals)
        return result

