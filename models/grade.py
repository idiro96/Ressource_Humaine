# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from werkzeug.routing import ValidationError


class RHGrade(models.Model):
    _name = 'rh.grade'
    _rec_name = 'intitule_grade'
    _order = "intitule_grade"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule_grade = fields.Char(required=True, track_visibility="onchange")
    intitule_grade_fr = fields.Char('Intitulé Grade', required=True, track_visibility="onchange")
    corps_id = fields.Many2one(comodel_name='rh.corps', track_visibility="onchange")
    filiere_id = fields.Many2one(comodel_name='rh.filiere', track_visibility="onchange")
    loi_id = fields.Many2one(comodel_name='rh.loi', track_visibility="onchange")
    grade_id = fields.Many2one('hr.groupe')
    categorie_id = fields.Many2one('rh.categorie', track_visibility="onchange")
    intitule = fields.Char(related='categorie_id.intitule', store=True)
    Indice_minimal = fields.Integer(related='categorie_id.Indice_minimal', store=True)
    employee_ids = fields.One2many('hr.employee', 'grade_id', string='Employees', groups='base.group_user')
    max_employee = fields.Integer(default=10, store=True, track_visibility="onchange")
    # nombre_de_postes_vacants = fields.Integer(compute='_compute_nombre_de_postes_vacants', store=True)
    description = fields.Char()
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')
    grade_lines = fields.One2many('rh.grade.line', inverse_name='grade_id', track_visibility='onchange')
    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHGrade, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHGrade, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHGrade, self).unlink()

    # @api.depends('employee_ids.grade_id', 'employee_ids.active', 'employee_ids.nature_travail_id', 'employee_ids.methode_embauche')
    # def _compute_employees(self):
    #     employee_data = self.env['hr.employee'].read_group(
    #         [
    #             ('grade_id', 'in', self.ids),
    #             ('nature_travail_id.code_type_fonction', '!=', 'postesuperieure'),
    #             ('nature_travail_id.code_type_fonction', '!=', 'fonctionsuperieure'),
    #         ],
    #         ['grade_id'],
    #         ['grade_id']
    #     )
    #     result = dict((data['grade_id'][0], data['grade_id_count']) for data in employee_data)
    #     for grade in self:
    #         grade.no_of_employee = result.get(grade.id, 0)
    #
    # @api.depends('employee_ids.grade_id', 'employee_ids.active', 'employee_ids.type_id.code_type_contract',
    #              'employee_ids.methode_embauche')
    # def _compute_employees_contract(self):
    #     contract_types = {
    #         'pleintemps_indeterminee': 'no_of_employee_cdi_plein',
    #         'pleintemps_determinee': 'no_of_employee_cdd_plein',
    #         'partiel_indeterminee': 'no_of_employee_cdi_partiel',
    #         'partiel_determinee': 'no_of_employee_cdd_partiel',
    #     }
    #
    #     for contract_type, field_name in contract_types.items():
    #         employee_data = self.env['hr.employee'].read_group(
    #             [
    #                 ('grade_id', 'in', self.ids),
    #                 ('type_id.code_type_contract', '=', contract_type),
    #                 ('methode_embauche', '=', 'recrutement')
    #             ],
    #             ['grade_id'], ['grade_id']
    #         )
    #         result = dict((data['grade_id'][0], data['grade_id_count']) for data in employee_data)
    #         for grade in self:
    #             setattr(grade, field_name, result.get(grade.id, 0))

    # @api.constrains('no_of_employee', 'max_employee')
    # def _check_max_employee_limit(self):
    #     for job in self:
    #         if job.no_of_employee > job.max_employee:
    #             raise ValidationError("لا يجوز أن عدد الموظفين يتفوق عن الحد الأقصى المسموح به")

    # @api.depends('max_employee', 'no_of_employee')
    # def _compute_nombre_de_postes_vacants(self):
    #     for job in self:
    #         job.nombre_de_postes_vacants = job.max_employee - job.no_of_employee
    #
    # @api.model
    # def create(self, vals):
    #     if vals.get('code', _('New')) == _('New'):
    #          vals['code'] = self.env['ir.sequence'].next_by_code('rh.grade.sequence') or _('New')
    #     result = super(RHGrade, self).create(vals)
    #     return result

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