# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHFormation(models.Model):
    _name = 'rh.formation'
    _rec_name = 'intitule_formation'
    _order = "date_debut_formation desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code_for = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_formation = fields.Char(track_visibility='onchange')
    date_debut_formation = fields.Date(track_visibility='onchange')
    date_fin_formation = fields.Date(track_visibility='onchange')
    lieu_formation = fields.Char(track_visibility='onchange')
    salle_formation = fields.Char(track_visibility='onchange')
    budget_allouee_formation = fields.Float(track_visibility='onchange')
    type_formation_id = fields.Many2one('rh.type.formation', track_visibility='onchange')
    organisme_id = fields.Many2one('rh.organisme', track_visibility='onchange')
    formation_lines = fields.One2many('rh.formation.line', inverse_name='formation_id', tracking=True)
    formation_absence = fields.One2many('rh.absence.formation', inverse_name='formation_id')
    formation_file_lines = fields.One2many('rh.file', 'formation_id')
    state = fields.Selection([('draft', 'Brouillon'), ('confirm', 'Validé'), ], readonly=True, default='draft')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHFormation, self).create(vals)

    @api.multi
    def write(self, vals):
        # if 'formation_lines' in vals:
        #     old_values = self.mapped('formation_lines').ids
        #     new_values = vals.get('formation_lines') and vals['formation_lines'][0][2]
        #
        #     added_values = list(set(new_values) - set(old_values)) if new_values else []
        #     removed_values = list(set(old_values) - set(new_values)) if new_values else []
        #
        #     message_body = ''
        #
        #     if added_values:
        #         message_body += "Added records: %s\n" % ', '.join(map(str, added_values))
        #
        #     if removed_values:
        #         message_body += "Removed records: %s\n" % ', '.join(map(str, removed_values))
        #
        #     if message_body:
        #         self.message_post(body=message_body, subtype='mail.mt_comment',
        #                           message_type='comment', author_id=self.env.user.id,
        #                           partner_ids=[(4, self.env.user.partner_id.id)])
        vals['write_uid'] = self.env.user.id
        return super(RHFormation, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.state in ['confirm']:
                raise ValidationError('You cannot delete a record that is confirmed or refused.')
        return super(RHFormation, self).unlink()

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def formation_detail_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'تفاصيل التكوين',
            'view_mode': 'form',
            'res_model': 'formation.detail',
        }

    @api.model
    def create(self, vals):
        if vals.get('code_for', _('New')) == _('New'):
            vals['code_for'] = self.env['ir.sequence'].next_by_code('rh.formation.sequence') or _('New')
        result = super(RHFormation, self).create(vals)
        return result

    @api.constrains('date_debut_formation', 'date_fin_formation', 'formation_lines')
    def _check_contract_overlap(self):
        for formation in self:
            for line in formation.formation_lines:
                employee = line.employee_id
                date_start = line.date_debut_formation_line
                date_end = line.date_fin_formation_line

                if not (formation.date_debut_formation <= date_start <= formation.date_fin_formation) or \
                        not (formation.date_debut_formation <= date_end <= formation.date_fin_formation):
                    raise ValidationError("la date doit étre compris dans l'intervale")

                # Check for overlapping formations for each employee
                overlapping_formations = self.search([
                    ('formation_lines.employee_id', '=', employee.id),
                    ('formation_lines.date_debut_formation_line', '<=', date_end),
                    ('formation_lines.date_fin_formation_line', '>=', date_start),
                    ('id', '!=', formation.id),
                ])
                if overlapping_formations:
                    raise ValidationError("vous avez sélectioner des employees en qui sont déja en formation")

    # @api.constrains('formation_lines')
    # def _check_contract_overlap(self):
    #     for formation in self:
    #         for line in formation.formation_lines:
    #             employee = line.employee_id
    #             date_start = line.date_debut_formation_line
    #             date_end = line.date_fin_formation_line
    #
    #             overlapping_formations = self.search([
    #                 ('formation_lines.employee_id', '=', employee.id),
    #                 ('formation_lines.date_debut_formation_line', '<=', date_end),
    #                 ('formation_lines.date_fin_formation_line', '>=', date_start),
    #                 ('id', '!=', formation.id),
    #             ])
    #             if overlapping_formations:
    #                 raise ValidationError("vous avez sélectioner des employees en qui sont déja en formation")
