# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError, UserError


class RHFinRelation(models.Model):
    _name = 'rh.fin.relation'
    _rec_name = 'employee_id'

    date_fin_relation = fields.Date()
    num_decision_fin_relation = fields.Char()
    type_fin_relation_id = fields.Many2one('rh.type.fin.relation')
    employee_id = fields.Many2one('hr.employee')
    fin_relation_file_lines = fields.One2many('rh.file', 'fin_relation_id')

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
