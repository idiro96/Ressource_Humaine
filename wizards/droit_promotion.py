# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class RHDroitPromotion(models.TransientModel):
    _name = 'droit.promotion'


    date_promotion = fields.Date()
    code = fields.Char()
    duree_promotion = fields.Selection([('5', '5'),
                              ('7', '7'),('10', '10'),],
                             readonly=False, default='5 ans')


    @api.multi
    def actualiser_droit_promotion(self):

        employee = self.env['hr.employee'].search([])
        promotion_ligne_droit = self.env['rh.promotion.droit'].search([])
        for record in promotion_ligne_droit:
            if record.sauvegarde == False:
                record.unlink()

        promotion_line = self.env['hr.employee'].search(
                [('date_grade', '<=', self.date_promotion)],
                order='date_grade DESC')
        if promotion_line:
            for promo in promotion_line:
                promotion_ligne_droit2 = self.env['rh.promotion.droit'].search(
                    [('employee_id', '=', promo.id), ('date_promotion', '=', self.date_promotion)])
                if not promotion_ligne_droit2:
                    dateDebut_object = fields.Date.from_string(self.date_promotion)
                    dateDebut_object2 = fields.Date.from_string(promo.date_grade)
                    difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # date_new_grade = relativedelta(months=60) + fields.Date.from_string(promo.date_grade)
                    # dateDebut_object3 = fields.Date.from_string(date_new_grade)
                    # duree = (dateDebut_object3.year - promo.date_grade.year) * 12 + dateDebut_object3.month - dateDebut_object2.month
                    print(int(self.duree_promotion) * 12)
                    if difference >= int(self.duree_promotion) * 12:
                        print('rabahni')
                        print(difference)
                        print(promo.name)
                        self.env['rh.promotion.droit'].create({
                            'employee_id': promo.id,
                            'type_fonction_id': promo.nature_travail_id.id,
                            'job_id': promo.job_id.id,
                            'duree': promo.job_id.id,
                            'date_promotion': self.date_promotion,
                            'grade_id': promo.grade_id.id,
                            'date_grade': promo.date_grade,
                            'grade_new_id': promo.grade_id.id,
                            'date_new_grade': relativedelta(months=int(self.duree_promotion) * 12) + fields.Date.from_string(promo.date_grade),
                            'duree': int(self.duree_promotion) * 12,
                        })

        return {
            'name': 'Droit Promotion',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'rh.promotion.droit',
            'type': 'ir.actions.act_window',
            # 'domain': [('date_new_grade', '=', self.date_promotion), ('sauvegarde', '=', True)]
            # 'domain': [('state', '=', 'reforme')],

        }








