# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RHTypeArretSalaire(models.Model):
    _name = 'rh.type.arret.salaire'
    _rec_name = 'description'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    description = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.arret.salaire.sequence') or _('New')
        result = super(RHTypeArretSalaire, self).create(vals)
        return result

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHTypeArretSalaire, self).unlink()