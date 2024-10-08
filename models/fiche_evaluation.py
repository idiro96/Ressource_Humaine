# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'
    _rec_name = 'exercice'
    _order = "exercice"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    date_evaluation = fields.Date(required=True, store=True, track_visibility='onchange')
    # employee_id = fields.Many2one('hr.employee', required=True, store=True, track_visibility='onchange')
    # grade_id = fields.Many2one('rh.grade', compute='_onchange_employee_id', store=True)
    # job_id = fields.Many2one('hr.job', compute='_onchange_employee_id', store=True)
    # echelon_id = fields.Many2one('rh.echelon', compute='_onchange_employee_id', store=True)
    # date_grade = fields.Date()
    # note = fields.Integer(default='20', track_visibility='onchange')
    # observation = fields.Char(track_visibility='onchange')
    fiche_evaluation_file = fields.Binary(track_visibility='onchange')
    exercice = fields.Integer(compute='_compute_exercice', store=True)
    # annee = exercice
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')
    fiche_evaluation_lines = fields.One2many('rh.fiche.evaluation.line', 'fiche_evaluation_id')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHFicheEvaluation, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHFicheEvaluation, self).write(vals)

    @api.multi
    def unlink(self):
        raise UserError("لا يمكنك حذف هذا التسجيل")
        return super(RHFicheEvaluation, self).unlink()

    @api.model
    def create(self, vals):
        # recalculer la valeur de "exercice"
        if vals.get('date_evaluation'):
            date_str = vals['date_evaluation']
            exercice = datetime.strptime(date_str, '%Y-%m-%d').year
            # verifier l'existance de l'enregistrement
            evaluation = self.env['rh.fiche.evaluation'].search([('exercice', '=', exercice)])
            if evaluation:
                raise UserError("يوجد إستمارة تنقيط بالفعل لهذا التمرين!")
            else:
                evalutation = super(RHFicheEvaluation, self).create(vals)
                return evalutation
        else:
            raise UserError("Entrer la date d'evaluation !")

    # @api.depends('employee_id')
    # def _onchange_employee_id(self):
    #     for rec in self:
    #         rec.grade_id = rec.employee_id.grade_id
    #         rec.job_id = rec.employee_id.job_id
    #         rec.echelon_id = rec.employee_id.echelon_id

    @api.depends('date_evaluation')
    def _compute_exercice(self):
        for rec in self:
            print('teste')
            if rec.date_evaluation:
                date_str = rec.date_evaluation
                rec.exercice = datetime.strptime(date_str, '%Y-%m-%d').year
                evaluation = self.env['rh.fiche.evaluation'].search([('exercice', '=', rec.exercice)])
                if evaluation:
                    raise UserError("يوجد إستمارة تنقيط بالفعل لهذا التمرين!")

    @api.model
    def create(self, vals):
        evaluation = super(RHFicheEvaluation, self).create(vals)
        employee = self.env['hr.employee'].search(
            [('code_type_fonction', '!=', 'contractuel'), ('fin_relation', '=', False)], order='name')
        for rec in employee:
            fiche_evaluation_line = self.env['rh.fiche.evaluation.line'].create({
                'employee_id': rec.id,
                'fiche_evaluation_id': evaluation.id,
            })
        return evaluation


class RHFicheEvaluationLine(models.Model):
    _name = 'rh.fiche.evaluation.line'
    _rec_name = 'employee_id'

    fiche_evaluation_id = fields.Many2one('rh.fiche.evaluation', tracking=True)
    employee_id = fields.Many2one('hr.employee')
    duree = fields.Selection(selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')],
                             default='inferieure')
    note = fields.Integer(default='20', track_visibility='onchange')
    observation = fields.Char(track_visibility='onchange')
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='always')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='always')

    @api.constrains('note')
    def chek_notation(self):
        for rec in self:
            if rec.note > 20:
                raise UserError("يجب أن يكون التنقيط بين 0 و 20!")

    @api.constrains('employee_id')
    def _check_duplicate_employee(self):
        for rec in self:
            existing_employees = self.search([
                ('fiche_evaluation_id', '=', rec.fiche_evaluation_id.id),
                ('employee_id', '=', rec.employee_id.id),
                ('id', '!=', rec.id)
            ])
            if existing_employees:
                employee_name = rec.employee_id.name
                raise ValidationError(f'لا يمكنك إضافة الموظف {employee_name} مرتين!')
