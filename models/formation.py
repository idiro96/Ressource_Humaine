# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHFormation(models.Model):
    _name = 'rh.formation'

    code_for = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_formation = fields.Char()
    date_debut_formation = fields.Date()
    date_fin_formation = fields.Date()
    lieu_formation = fields.Char()
    salle_formation = fields.Char()
    budget_allouee_formation = fields.Float()
    type_formation_id = fields.Many2one('rh.type.formation')
    organisme_id = fields.Many2one('rh.organisme')
    formation_lines = fields.One2many('rh.formation.line', inverse_name='formation_id', string="Formation Lines")
    formation_absence = fields.One2many('rh.absence.formation', inverse_name='formation_id', string="Formation Absence")
    formation_file_lines = fields.One2many('rh.file', 'formation_id')

    def formation_detail_wizard(self):
        return {
        'type': 'ir.actions.act_window',
        'target': 'new',
        'name': 'Formation detail',
        'view_mode': 'form',
        'res_model': 'formation.detail',
        }


    @api.model
    def create(self, vals):
        if vals.get('code_for', _('New')) == _('New'):
             vals['code_for'] = self.env['ir.sequence'].next_by_code('rh.formation.sequence') or _('New')
        result = super(RHFormation, self).create(vals)
        return result

