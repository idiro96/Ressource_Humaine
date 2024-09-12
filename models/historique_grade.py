# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHhistorique_grade(models.Model):
    _name = 'rh.historique.grade'
    _rec_name = 'grade'

    grade = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    date_debut_travail = fields.Date()
    anne_debut_travail = fields.Char()
    is_year = fields.Boolean(default=True)
    document_file_line = fields.Binary()



    # @api.multi
    # def changer_type(self):
    #     print(self.active)
    #     for record in self:
    #         print('ttttttttttt')
    #         print(record.active)
    #         record.active = not record.active
    #         print(record.active)


