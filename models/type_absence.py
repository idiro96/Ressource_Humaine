# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHTypeAbsence(models.Model):
    _name = 'rh.type.absence'

    code_type_absence = fields.Char(String='Code type absence', readonly=True, default=lambda self: _('New'))
    intitule_type_absence = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code_type_absence', _('New')) == _('New'):
             vals['code_type_absence'] = self.env['ir.sequence'].next_by_code('rh.type.absence.sequence') or _('New')
        result = super(RHTypeAbsence, self).create(vals)
        return result

