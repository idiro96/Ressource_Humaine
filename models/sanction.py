# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHSanction(models.Model):
    _name = 'rh.sanction'

    code_sanction = fields.Char()
    ref_pv_sanction = fields.Char()
    date_pv_sanction = fields.Date()
    num_decision_sanction = fields.Char()
    date_decision_sanction = fields.Date()
    type_faute_id = fields.Many2one('rh.type.faute')
    type_sanction_id = fields.Many2one('rh.type.sanction')
    employee_id = fields.Many2one('hr.employee')
    choisir_commission_lines = fields.One2many('rh.commission.line', 'sanction_id')
    sanction_file_lines = fields.One2many('rh.file', 'sanction_id')



    @api.model
    def create(self, vals):
        if vals.get('code_sanction', _('New')) == _('New'):
             vals['code_sanction'] = self.env['ir.sequence'].next_by_code('rh.sanction.sequence') or _('New')
        result = super(RHSanction, self).create(vals)
        return result


    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Choisir Commission',
            'view_mode': 'form',
            'res_model': 'choisir.commission',
        }

