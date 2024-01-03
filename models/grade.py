# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHGrade(models.Model):
    _name = 'rh.grade'
    _rec_name = 'intitule_grade'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_grade = fields.Char()
    corps_id = fields.Many2one(comodel_name='rh.corps')
    filiere_id = fields.Many2one(comodel_name='rh.filiere')
    loi_id = fields.Many2one(comodel_name='rh.loi')
    grade_id = fields.Many2one('hr.groupe')


    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
             vals['code'] = self.env['ir.sequence'].next_by_code('rh.grade.sequence') or _('New')
        result = super(RHGrade, self).create(vals)
        return result

    @api.onchange('loi_id')
    def onchange_loi_id(self):
        if self.loi_id:
            filiere_domain = [('loi_id', '=', self.loi_id.id)]
            corps_domain = [('loi_id', '=', self.loi_id.id)]
            if self.filiere_id:
                filiere_domain.append(('id', '=', self.filiere_id.id))
                corps_domain.append(('filiere_id', '=', self.filiere_id.id))
            return {'domain': {'filiere_id': filiere_domain, 'corps_id': corps_domain}}
        else:
            return {'domain': {'filiere_id': [], 'corps_id': []}}

    @api.onchange('filiere_id')
    def onchange_filiere_id(self):
        if self.filiere_id:
            return {'domain': {'corps_id': [('filiere_id', '=', self.filiere_id.id)]}}
        else:
            return {'domain': {'corps_id': []}}

    # @api.onchange('loi_id')
    # def _onchange_related_field_loi(self):
    #     # This method will be called when the value of 'related_field' changes
    #     # Update the domain for 'field1' based on the value of 'related_field'
    #     print('teste')
    #     for rec in self:
    #         domain = []
    #         if rec.loi_id:
    #             print('teste')
    #             filiere = self.env['rh.filiere'].search([('loi_id', '=', rec.loi_id.id)])
    #             print(filiere)
    #             domain.append(('id', 'in', filiere.ids))
    #         else:
    #             domain = ''
    #
    #     res = {'domain': {'filiere_id': domain}}
    #     print(res)
    #     return res
    #
    # @api.onchange('filiere_id')
    # def _onchange_related_field_filier(self):
    #     print('teste')
    #     for rec in self:
    #         domain = []
    #         if rec.filiere_id:
    #             print('teste')
    #             corps = self.env['rh.corps'].search([('filiere_id', '=', rec.filiere_id.id)])
    #             print(corps)
    #             if not rec.filiere_id:
    #                 corps = self.env['rh.corps'].search([('loi_id', '=', rec.loi_id.id)])
    #                 domain.append(('id', 'in', corps.ids))
    #         else:
    #             domain = ''
    #
    #     res = {'domain': {'corps_id': domain}}
    #     print(res)
    #     return res