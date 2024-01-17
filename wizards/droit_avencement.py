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
        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_droit = self.env['rh.avencement.droit'].search([])
        for record in avancement_ligne_droit:
            record.unlink()
        for rec in employee:

            avancement_line = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.id), ('date_avancement', '<=', self.date_avancement)],
                order='date_avancement DESC', limit=1)
            if avancement_line:
                for avance in avancement_line:
                    dateDebut_object = fields.Date.from_string(self.date_avancement)
                    print(avance.date_avancement)
                    dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                    difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # difference = dateDebut_object - dateDebut_object2
                    print(difference)
                    print('difference')
                    if difference >= 30 and rec.nature_travail_id.code_type_fonction == 'fonction':
                        self.env['rh.avencement.droit'].create({
                            'employee_id': avancement_line.employee_id.id,
                            'type_fonction_id': rec.nature_travail_id.id,
                            'groupe_old_id': avancement_line.groupe_old_id.id,
                            'categorie_old_id': avancement_line.categorie_old_id.id,
                            'echelon_old_id': avancement_line.echelon_old_id.id,

                            'groupe_new_id': avancement_line.groupe_old_id.id,
                            'categorie_new_id': avancement_line.categorie_old_id.id,
                            'echelon_new_id': avancement_line.echelon_old_id.id

                        })
                    elif difference >= 24 and rec.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                        self.env['rh.avencement.droit'].create({
                            'employee_id': avancement_line.employee_id.id,
                            'type_fonction_id': rec.nature_travail_id.id,
                            'categorie_old_id': avancement_line.categorie_old_id.id,
                            'section_old_id': avancement_line.section_old_id.id,
                            'echelon_old_id': avancement_line.echelon_old_id.id,


                            'categorie_new_id': avancement_line.categorie_old_id.id,
                            'section_new_id': avancement_line.section_old_id.id,
                            'echelon_new_id': avancement_line.echelon_old_id.id,

                        })
                    elif difference >= 24 and rec.nature_travail_id.code_type_fonction == 'postesuperieure':
                        self.env['rh.avencement.droit'].create({
                            'employee_id': avancement_line.employee_id.id,
                            'type_fonction_id': rec.nature_travail_id.id,
                            'groupe_old_id': avancement_line.groupe_old_id.id,
                            'categorie_old_id': avancement_line.categorie_old_id.id,
                            'echelon_old_id': avancement_line.echelon_old_id.id,
                            'categorie_superieure_old_id': avancement_line.categorie_superieure_old_id.id,
                            'section_superieure_old_id': avancement_line.section_superieure_old_id.id,
                            'niveau_hierarchique_old_id': avancement_line.niveau_hierarchique_old_id.id,

                            'groupe_new_id': avancement_line.groupe_old_id.id,
                            'categorie_new_id': avancement_line.categorie_old_id.id,
                            'echelon_new_id': avancement_line.echelon_old_id.id,
                            'categorie_superieure_new_id': avancement_line.categorie_superieure_old_id.id,
                            'section_superieure_new_id': avancement_line.section_superieure_old_id.id,
                            'niveau_hierarchique_new_id': avancement_line.niveau_hierarchique_old_id.id
                        })


        return {
            'name': 'Droit Avancement',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.avencement.droit',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }








