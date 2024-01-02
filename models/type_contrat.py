# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeContrat(models.Model):
    _name = 'rh.type.contrat'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_contrat = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.contrat.sequence') or _('New')
        result = super(RHTypeContrat, self).create(vals)
        return result

