# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitAvencement(models.TransientModel):
    _name = 'droit.avencement'

    # employee_id = fields.Many2one('hr.employee')
    # groupe_old_id = fields.Many2one('rh.groupe')
    # categorie_old_id = fields.Many2one('rh.categorie')
    # section_old_id = fields.Many2one('rh.section')
    # echelon_old_id = fields.Many2one('rh.echelon')

    date_avancement = fields.Date()
    code = fields.Char()
    # avancement_lines = fields.One2many('rh.avancement.line', inverse_name='avancement_id')
    # avancement_lines_wizard = fields.One2many('rh.avancement.line.wizard', inverse_name='avancement_id')

    @api.multi
    def actualiser_droit_avencement(self):
        print('glllllllllll')
        print('teste')
        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_droit = self.env['rh.avencement.droit'].search([])
        for record in avancement_ligne_droit:
            record.unlink()
        for rec in employee:
            print(rec.id)

            avancement_line = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.id), ('date_avancement', '<=', self.date_avancement)],
                order='date_avancement desc', limit=1)
            if avancement_line:
                for avance in avancement_line:
                    dateDebut_object = fields.Date.from_string(self.date_avancement)
                    dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                    difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # difference = dateDebut_object - dateDebut_object2
                    print(difference)
                    print('difference')
                    if difference >= 30:
                        self.env['rh.avencement.droit'].create({
                            'employee_id': avancement_line.employee_id.id,
                            'categorie_new_id': avancement_line.categorie_new_id.id,
                            'section_new_id': avancement_line.section_new_id.id,
                            'echelon_new_id': avancement_line.echelon_new_id.id

                        })
        # self.avancement_lines_wizard = self.env['rh.avancement.line.wizard'].search([])

        return {
            'name': 'Droit Avancement',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.avencement.droit',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }








