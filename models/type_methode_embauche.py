
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class RHTypeMethodeEmbauche(models.Model):
    _name = 'rh.type.methode.embauche'
    _rec_name = "description_type_embauche"



    type_embauche = fields.Char()
    description_type_embauche = fields.Char()

    def unlink(self):
        for rec in self:
            raise UserError(
                    "لا يمكنك حذف هذا التسجيل")
        return super(RHTypeMethodeEmbauche, self).unlink()




