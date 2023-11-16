# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHVisiteMedicale(models.Model):

    _name = 'rh.visite.medicale'
    _rec_name = 'code_visite_medicale'


    code_visite_medicale = fields.Char()
    date_debut_visite_medicale = fields.Date()
    date_fin_visite_medicale = fields.Date()
    cout_visite_medicale = fields.Float()
    cabinet_medical_id = fields.Many2one('rh.cabinet.medical')
    visite_medical_lines = fields.One2many('rh.visite.medical.line', 'visite_medical_id', string="Visite Medical Lines")


    @api.model
    def create(self, vals):
        if vals.get('code_visite_medicale', _('New')) == _('New'):
             vals['code_visite_medicale'] = self.env['ir.sequence'].next_by_code('') or _('New')
        result = super(RHVisiteMedicale, self).create(vals)
        return result

    def visite_medical_detaille(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'visite medical detaille',
            'view_mode': 'form',
            'res_model': 'visite.medical.detaille',
        }









