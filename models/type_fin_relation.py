# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeFinRelation(models.Model):
    _name = 'rh.type.fin.relation'

    code = fields.Char(String='Code', readonly=True, default=lambda self: _('New'))
    code_type_fin_relation = fields.Date()



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.fin.relation.sequence') or _('New')
        result = super(RHTypeFinRelation, self).create(vals)
        return result




