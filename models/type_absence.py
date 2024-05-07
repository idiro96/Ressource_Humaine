
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError




class RHTypeAbsence(models.Model):
    _name = 'rh.type.absence'
    _rec_name = "intitule_type_absence"



    code_type_absence = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_type_absence = fields.Char()




    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHTypeAbsence, self).unlink()