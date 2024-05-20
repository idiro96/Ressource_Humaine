
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class RHTypeConge(models.Model):
    _name = 'rh.type.conge'
    _rec_name = "intitule_type_conge"



    code_type_conge = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_type_conge = fields.Char()




    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHTypeConge, self).unlink()