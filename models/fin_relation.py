# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError, UserError


class RHFinRelation(models.Model):
    _name = 'rh.fin.relation'
    _rec_name = 'employee_id'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code_promotion = fields.Char(compute="_compute_code", store=True)
    date_promotion = fields.Char(compute="_compute_code", store=True)
    date_fin_relation = fields.Date(track_visibility='onchange')
    num_decision_fin_relation = fields.Char(track_visibility='onchange')
    type_fin_relation_id = fields.Many2one('rh.type.fin.relation', track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', domain="[('fin_relation', '=', False)]", track_visibility='onchange')
    fin_relation_file_lines = fields.One2many('rh.file', 'fin_relation_id')
    description = fields.Char(related='type_fin_relation_id.description')
    date_cnas = fields.Date(track_visibility='onchange')
    date_decision_fin_relation = fields.Date(track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHFinRelation, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHFinRelation, self).write(vals)

    @api.depends('employee_id')
    def _compute_code(self):
        for rec in self:
            promotion_line = self.env['rh.promotion.line'].search(
                [('employee_id', '<=', rec.employee_id.id)],
                order='date_new_grade DESC', limit=1)
            for rec1 in promotion_line:

                promotion = self.env['rh.promotion'].search(
                    [('id', '<=', rec1.promotion_id.id)],
                    order='date_new_grade DESC', limit=1)

                if promotion:
                    rec.code_promotion = promotion.code
                    rec.date_promotion = promotion.date_promotion

    @api.constrains('employee_id', 'type_fin_relation_id')
    def _check_employee_age(self):
        for record in self:
            employee = record.employee_id
            age = employee.age_employee
            gender = employee.gender

            if (
                    (
                            gender == 'male' and age < record.type_fin_relation_id.age_male and record.type_fin_relation_id.description_fr == 'Départ en Retraite') or
                    (
                            gender == 'female' and age < record.type_fin_relation_id.age_female and record.type_fin_relation_id.description_fr == 'Départ en Retraite')
            ):
                raise UserError(_("لا يمكن أن عمر الموظف يكون أقل من السن المطلوب للتقاعد!"))

    @api.model
    def create(self, vals):
        fin_relation = super(RHFinRelation, self).create(vals)

        employee = self.env['hr.employee'].search(
            [('id', '=', vals['employee_id'])])
        print('qdqs')
        print(employee)
        employee.write({
            'fin_relation': True,
        })
        employee.write({
            'date_fin_relation': vals['date_fin_relation'],
        })
        return fin_relation

    def action_arret_de_salaire(self):
        print()
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'decision arret salaire',
            'view_mode': 'form',
            'res_model': 'arret.salaire',
        }
