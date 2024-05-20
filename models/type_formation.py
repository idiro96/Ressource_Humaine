# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class RHTypeFormation(models.Model):
    _name = 'rh.type.formation'
    _rec_name = 'description_type_formation'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    description_type_formation = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.formation.sequence') or _('New')
        result = super(RHTypeFormation, self).create(vals)
        return result

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHTypeFormation, self).unlink()