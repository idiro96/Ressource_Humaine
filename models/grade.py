# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHGrade(models.Model):
    _name = 'rh.grade'

    code = fields.Char(String='Code', readonly=True, default=lambda self: _('New'))
    intitule_grade = fields.Char()
    secteure_id = fields.Many2one(comodel_name='rh.secteure')



    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.grade.sequence') or _('New')
        result = super(RHGrade, self).create(vals)
        return result

