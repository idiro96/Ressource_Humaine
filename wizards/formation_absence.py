# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAbsenceFormation(models.TransientModel):
    _name = 'absence.formation'

    date_absence = fields.Date()

    def absence_formation(self):
        record = self.env['rh.formation.line'].browse(self._context['active_id'])
        for line in record:
            absence_formation = self.env['rh.absence.formation'].create({
                    'employee_id': line.employee_id.id,
                    'formation_line_id': line.id,
                    'formation_id': line.formation_id.id,
                    'date_absence': self.date_absence
                })