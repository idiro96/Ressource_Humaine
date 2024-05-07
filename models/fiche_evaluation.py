# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class RHFicheEvaluation(models.Model):
    _name = 'rh.fiche.evaluation'
    _order = "employee_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    date_evaluation = fields.Date(required=True, store=True, track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', required=True, store=True, track_visibility='onchange')
    grade_id = fields.Many2one('rh.grade', compute='_onchange_employee_id', store=True)
    job_id = fields.Many2one('hr.job', compute='_onchange_employee_id', store=True)
    echelon_id = fields.Many2one('rh.echelon', compute='_onchange_employee_id', store=True)
    date_grade = fields.Date()
    note = fields.Integer(track_visibility='onchange')
    observation = fields.Char(track_visibility='onchange')
    fiche_evaluation_file = fields.Binary(track_visibility='onchange')
    exercice = fields.Integer(compute='_compute_exercice', store=True)
    # annee = exercice
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHFicheEvaluation, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHFicheEvaluation, self).write(vals)

    @api.model
    def create(self, vals):
        # recalculer la valeur de "exercice"
        if vals.get('date_evaluation'):
            date_str = vals['date_evaluation']
            exercice = datetime.strptime(date_str, '%Y-%m-%d').year
            # verifier l'existance de l'enregistrement
            evaluation = self.env['rh.fiche.evaluation'].search(
                [('employee_id', '=', vals['employee_id']), ('exercice', '=', exercice)])
            if evaluation:
                raise UserError("L employee choisit possède déja une notation pour cet exercice")
            else:
                evalutation = super(RHFicheEvaluation, self).create(vals)
                return evalutation
        else:
            raise UserError("Entrer la date d'evaluation")

    @api.depends('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            rec.grade_id = rec.employee_id.grade_id
            rec.job_id = rec.employee_id.job_id
            rec.echelon_id = rec.employee_id.echelon_id

    @api.depends('date_evaluation')
    def _compute_exercice(self):
        for rec in self:
            print('teste')
            if rec.date_evaluation:
                date_str = rec.date_evaluation
                rec.exercice = datetime.strptime(date_str, '%Y-%m-%d').year
                evaluation = self.env['rh.fiche.evaluation'].search(
                    [('employee_id', '=', rec.employee_id.id), ('exercice', '=', rec.exercice)])
                if evaluation:
                    raise UserError("L employee choisit possède déja une notation pour cet exercice")

