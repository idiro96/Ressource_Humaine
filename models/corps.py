# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHSecteure(models.Model):
    _name = 'rh.corps'
    _rec_name = 'intitule_corps'


    code = fields.Char(String='Code', readonly=True, default=lambda self: _('New'))
    intitule_corps= fields.Char()
    filiere_id = fields.Many2one(comodel_name='rh.filiere')
    loi_id = fields.Many2one(comodel_name='rh.loi')



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.corps.sequence') or _('New')
        result = super(RHSecteure, self).create(vals)
        return result

