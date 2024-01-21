# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitAvencement(models.TransientModel):
    _name = 'droit.avencement'


    date_avancement = fields.Date()
    code = fields.Char()



    @api.multi
    def Archiver(self):
        print('glllllllllll')
        self.sauvegarde = True


    @api.multi
    def actualiser_droit_avencement(self):
        print('glllllllllll')
        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_droit = self.env['rh.avencement.droit'].search([])
        for record in avancement_ligne_droit:
            if record.sauvegarde == False:
                record.unlink()

        avancement_line = self.env['hr.employee'].search(
                [('date_avancement', '<=', self.date_avancement)],
                order='date_avancement DESC')
        if avancement_line:
            for avance in avancement_line:
                    avancement_ligne_droit2 = self.env['rh.avencement.droit'].search([('employee_id', '=', avance.id),('date_avancement', '=', self.date_avancement)])
                    if not avancement_ligne_droit2:
                        dateDebut_object = fields.Date.from_string(self.date_avancement)
                        print(avance.date_avancement)
                        dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                        difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month

                        if difference >= 30 and avance.nature_travail_id.code_type_fonction == 'fonction':
                                self.env['rh.avencement.droit'].create({
                                    'employee_id': avance.id,
                                    'type_fonction_id': avance.nature_travail_id.id,
                                    'date_avancement': self.date_avancement,
                                    'date_old_avancement': avance.date_avancement,
                                    'grade_id': avance.grade_id.id,
                                    'job_id': avance.job_id.id,
                                    'groupe_old_id': avance.groupe_id.id,
                                    'categorie_old_id': avance.categorie_id.id,
                                    'echelon_old_id': avance.echelon_id.id,

                                    'groupe_new_id': avance.groupe_id.id,
                                    'categorie_new_id': avance.categorie_id.id,
                                    'echelon_new_id': avance.echelon_id.id
                                    })

                        elif difference >= 24 and avance.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                                self.env['rh.avencement.droit'].create({
                                    'employee_id': avance.id,
                                    'type_fonction_id': avance.nature_travail_id.id,
                                    'date_avancement': self.date_avancement,
                                    'date_old_avancement': avance.date_avancement,
                                    'grade_id': avance.grade_id.id,
                                    'job_id': avance.job_id.id,
                                    'categorie_old_id': avance.categorie_id.id,
                                    'section_old_id': avance.section_id.id,
                                    'echelon_old_id': avance.echelon_id.id,

                                    'categorie_new_id': avance.categorie_id.id,
                                    'section_new_id': avance.section_id.id,
                                    'echelon_new_id': avance.echelon_id.id
                                    })

                        elif difference >= 24 and avance.nature_travail_id.code_type_fonction == 'postesuperieure':
                            self.env['rh.avencement.droit'].create({
                                'employee_id': avance.id,
                                'type_fonction_id': avance.nature_travail_id.id,
                                'date_avancement': self.date_avancement,
                                'date_old_avancement': avance.date_avancement,
                                'grade_id': avance.grade_id.id,
                                'job_id': avance.job_id.id,
                                'groupe_old_id': avance.groupe_id.id,
                                'categorie_old_id': avance.categorie_id.id,
                                'echelon_old_id': avance.echelon_id.id,
                                'categorie_superieure_old_id': avance.categorie_superieure_id.id,
                                'section_superieure_old_id': avance.section_superieure_id.id,
                                'niveau_hierarchique_old_id': avance.niveau_hierarchique_id.id,

                                'groupe_new_id': avance.groupe_id.id,
                                'categorie_new_id': avance.categorie_id.id,
                                'echelon_new_id': avance.echelon_id.id,
                                'categorie_superieure_new_id': avance.categorie_superieure_id.id,
                                'section_superieure_new_id': avance.section_superieure_id.id,
                                'niveau_hierarchique_new_id': avance.niveau_hierarchique_id.id
                            })


        return {
            'name': 'Droit Avancement',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.avencement.droit',
            'type': 'ir.actions.act_window',
            'domain': [('date_avancement', '=', self.date_avancement), ('sauvegarde', '=', True)],

        }








