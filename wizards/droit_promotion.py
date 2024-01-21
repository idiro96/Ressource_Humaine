# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitPromotion(models.TransientModel):
    _name = 'droit.promotion'


    date_promotion = fields.Date()
    code = fields.Char()


    @api.multi
    def actualiser_droit_promotion(self):

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
                    print(difference)
                    print(promo.name)
                    if difference >= 12:
                        self.env['rh.promotion.droit'].create({
                            'employee_id': promo.id,
                            'type_fonction_id': promo.nature_travail_id.id,
                            'grade_id': promo.grade_id.id,
                            'date_grade': promo.date_grade,
                            'grade_new_id': promo.date_new_grade,
                            'date_new_grade': promo.date_new_grade,
                        })

        return {
            'name': 'Droit Promotion',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.promotion.droit',
            'type': 'ir.actions.act_window',
            # 'domain': [('state', '=', 'reforme')],

        }








