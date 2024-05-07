# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class RHVisiteMedicale(models.Model):
    _name = 'rh.visite.medicale'
    _rec_name = 'code_visite_medicale'
    _order = "date_debut_visite_medicale desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code_visite_medicale = fields.Char(readonly=True, default=lambda self: _('New'))
    date_debut_visite_medicale = fields.Date(track_visibility='onchange')
    date_fin_visite_medicale = fields.Date(track_visibility='onchange')
    cout_visite_medicale = fields.Float(track_visibility='onchange')
    cabinet_medical_id = fields.Many2one('rh.cabinet.medical', track_visibility='onchange')
    visite_medical_lines = fields.One2many('rh.visite.medical.line', 'visite_medical_id')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHVisiteMedicale, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHVisiteMedicale, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('code_type_sanction', _('New')) == _('New'):
             vals['code_type_sanction'] = self.env['ir.sequence'].next_by_code('rh.type.sanction.sequence') or _('New')
        result = super(RHVisiteMedicale, self).create(vals)
        return result


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
            'name': 'تفاصيل الزيارة الطبية',
            'view_mode': 'form',
            'res_model': 'visite.medical.detaille',
        }
