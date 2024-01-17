# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitPromotion(models.TransientModel):
    _name = 'droit.promotion'

    # employee_id = fields.Many2one('hr.employee')
    # groupe_old_id = fields.Many2one('rh.groupe')
    # categorie_old_id = fields.Many2one('rh.categorie')
    # section_old_id = fields.Many2one('rh.section')
    # echelon_old_id = fields.Many2one('rh.echelon')

    date_promotion = fields.Date()
    code = fields.Char()
    # avancement_lines = fields.One2many('rh.avancement.line', inverse_name='avancement_id')
    # avancement_lines_wizard = fields.One2many('rh.avancement.line.wizard', inverse_name='avancement_id')

    @api.multi
    def actualiser_droit_promotion(self):
        print('glllllllllll')
        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        promotion_ligne_droit = self.env['rh.promotion.droit'].search([])
        for record in promotion_ligne_droit:
            record.unlink()

        promotion_line = self.env['hr.employee'].search(
                [('date_grade', '<=', self.date_promotion)],
                order='date_grade DESC')
        if promotion_line:
            for promo in promotion_line:
                    dateDebut_object = fields.Date.from_string(self.date_promotion)
                    dateDebut_object2 = fields.Date.from_string(promo.date_grade)
                    difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # difference = dateDebut_object - dateDebut_object2
                    if difference >= 12:
                        self.env['rh.promotion.droit'].create({
                            'employee_id': promo.id,
                            'type_fonction_id': promo.nature_travail_id.id,
                            'grade_id': promo.grade_id.id,
                            'date_grade': promo.date_grade,
                        })
                    # elif difference >= 24 and rec.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                    #     self.env['rh.avencement.droit'].create({
                    #         'employee_id': avancement_line.employee_id.id,
                    #         'type_fonction_id': rec.nature_travail_id.id,
                    #         'categorie_old_id': avancement_line.categorie_old_id.id,
                    #         'section_old_id': avancement_line.section_old_id.id,
                    #         'echelon_old_id': avancement_line.echelon_old_id.id,
                    #
                    #
                    #         'categorie_new_id': avancement_line.categorie_old_id.id,
                    #         'section_new_id': avancement_line.section_old_id.id,
                    #         'echelon_new_id': avancement_line.echelon_old_id.id,
                    #
                    #     })
                    # elif difference >= 24 and rec.nature_travail_id.code_type_fonction == 'postesuperieure':
                    #     self.env['rh.avencement.droit'].create({
                    #         'employee_id': avancement_line.employee_id.id,
                    #         'type_fonction_id': rec.nature_travail_id.id,
                    #         'groupe_old_id': avancement_line.groupe_old_id.id,
                    #         'categorie_old_id': avancement_line.categorie_old_id.id,
                    #         'echelon_old_id': avancement_line.echelon_old_id.id,
                    #         'categorie_superieure_old_id': avancement_line.categorie_superieure_old_id.id,
                    #         'section_superieure_old_id': avancement_line.section_superieure_old_id.id,
                    #         'niveau_hierarchique_old_id': avancement_line.niveau_hierarchique_old_id.id,
                    #
                    #         'groupe_new_id': avancement_line.groupe_old_id.id,
                    #         'categorie_new_id': avancement_line.categorie_old_id.id,
                    #         'echelon_new_id': avancement_line.echelon_old_id.id,
                    #         'categorie_superieure_new_id': avancement_line.categorie_superieure_old_id.id,
                    #         'section_superieure_new_id': avancement_line.section_superieure_old_id.id,
                    #         'niveau_hierarchique_new_id': avancement_line.niveau_hierarchique_old_id.id
                    #     })
                    #

        return {
            'name': 'Droit Promotion',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.promotion.droit',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }








