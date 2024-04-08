# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHSecteure(models.Model):
    _name = 'rh.corps'
    _rec_name = 'intitule_corps'
    _order = "intitule_corps"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_corps = fields.Char(track_visibility='onchange')
    filiere_id = fields.Many2one(comodel_name='rh.filiere', track_visibility='onchange')
    loi_id = fields.Many2one(comodel_name='rh.loi', track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHSecteure, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHSecteure, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.corps.sequence') or _('New')
        result = super(RHSecteure, self).create(vals)
        return result

    @api.onchange('loi_id')
    def _onchange_related_field(self):
        # This method will be called when the value of 'related_field' changes
        # Update the domain for 'field1' based on the value of 'related_field'
        print('teste')
        for rec in self:
            domain = []
            if rec.loi_id:
                print('teste')
                filiere = self.env['rh.filiere'].search([('loi_id', '=', rec.loi_id.id)])
                print(filiere)
                domain.append(('id', 'in', filiere.ids))
            else:
                domain = ''

        res = {'domain': {'filiere_id': domain}}
        print(res)
        return res
