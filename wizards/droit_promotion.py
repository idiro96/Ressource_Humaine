# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import UserError


class RHDroitPromotion(models.TransientModel):
    _name = 'droit.promotion'


    date_promotion = fields.Date()
    code = fields.Char()
    duree_promotion = fields.Selection([('5', '5'),
                              ('7', '7'),('10', '10'),],
                             readonly=False)
    boul = fields.Boolean(default=False)
    sauvegarde = fields.Boolean(default=False)

    # @api.constrains
    # @api.multi
    # def unlink(self):
    #     records = self.env['rh.promotion.droit'].browse(self._context['active_ids'])
    #     for rec in records:
    #         promotion_ligne = self.env['rh.promotion.ligne'].search(
    #             [('employee_id', '=', rec.employee_id.id), ('date_grade', '=', rec.date_new_grade)])
    #         if promotion_ligne:
    #             raise UserError("Enregistrement déja fait, vous ne pouvez pas le supprimer")


    @api.multi
    def actualiser_droit_promotion(self):
        if self.boul == False:
            promotion_line1 = None
            promotion_line2 = None
            promotion_line = None
            promotion_ligne3 = None
            promotion_ligne_droit = self.env['rh.promotion.droit'].search([])
            for record in promotion_ligne_droit:
                if record.sauvegarde == False:
                    record.unlink()
            nature_travail = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonction')])
            nature_travail_superieure = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonctionsuperieure')])
            if self.duree_promotion == '5':
                promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion),('indice_minimal', '<', 821),('nature_travail_id', '=', nature_travail.id),('fin_relation', '=', False)],
                        order='date_grade DESC')
                print('<821')
            elif self.duree_promotion == '7':
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', self.date_promotion), ('indice_minimal', '>=', 821),('nature_travail_id', '=', nature_travail.id),('fin_relation', '=', False)],
                    order='date_grade DESC')
                print('>821')
            else:
                dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', dateDebut_object10),('fin_relation', '=', False),('nature_travail_id', '=', nature_travail.id),('promotion_dix', '=', False)],
                    order='date_grade DESC')
                print('+10')

            if self.duree_promotion == '5':
                promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion),('point_indiciare', '<', 4275),('nature_travail_id', '=', nature_travail_superieure.id),('fin_relation', '=', False)],
                        order='date_grade DESC')
                print('<821')
            elif self.duree_promotion == '7':
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', self.date_promotion), ('point_indiciare', '>=', 4275),('nature_travail_id', '=', nature_travail_superieure.id),('fin_relation', '=', False)],
                    order='date_grade DESC')
                print('>821')
            else:
                dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', dateDebut_object10),('fin_relation', '=', False),('nature_travail_id', '=', nature_travail_superieure.id),('promotion_dix', '=', False)],
                    order='date_grade DESC')
            if  promotion_line1 and promotion_line2:
                promotion_line = promotion_line1 + promotion_line2
            if  promotion_line1 and not promotion_line2:
                promotion_line = promotion_line1
            if  not promotion_line1 and promotion_line2:
                promotion_line = promotion_line2
            promotion_ligne3 = promotion_line
            if promotion_line:
                for rec in promotion_line:
                    print(rec.name)
                    promotion_ligne2 = self.env['rh.promotion.line'].search(
                    [('employee_id', '=', rec.id), ('date_promotion', '=', self.date_promotion)])
                    if promotion_ligne2:
                        promotion_ligne3 = promotion_ligne3 - rec


            if promotion_ligne3:
                promotion_line = promotion_ligne3
            if promotion_line:
                for promo in promotion_line:
                    promotion_ligne_droit2 = self.env['rh.promotion.droit'].search(
                        [('employee_id', '=', promo.id), ('date_promotion', '=', self.date_promotion)])
                    promotion_ligne_droit3 = self.env['rh.promotion.droit'].search(
                        [('employee_id', '=', promo.id), ('sauvegarde', '=', True),('retenue', '=', True)],order='date_grade DESC', limit=1)
                    if not promotion_ligne_droit2:
                        dateDebut_object = fields.Date.from_string(self.date_promotion)
                        dateDebut_object2 = fields.Date.from_string(promo.date_grade)
                        difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                        if difference >= int(self.duree_promotion) * 12:
                            if promotion_ligne_droit3:
                                if fields.Date.from_string(promotion_ligne_droit3.date_new_grade) == fields.Date.from_string(promo.date_grade):
                                    self.env['rh.promotion.droit'].create({
                                        'employee_id': promo.id,
                                        'type_fonction_id': promo.nature_travail_id.id,
                                        'job_id': promo.job_id.id,
                                        'duree': promo.job_id.id,
                                        'date_promotion': self.date_promotion,
                                        'grade_id': promo.grade_id.id,
                                        'categorie_id': promo.categorie_id.id,
                                        'date_grade': promo.date_grade,
                                        'grade_new_id': promo.grade_id.id,
                                        'date_new_grade': relativedelta(months=int(self.duree_promotion) * 12) + fields.Date.from_string(promo.date_grade),
                                        'duree': int(self.duree_promotion) * 12,
                                        'sauvegarde': self.sauvegarde,
                                        'retenue': self.sauvegarde
                                    })
                                else:
                                    print('employe existe')
                            else:
                                self.env['rh.promotion.droit'].create({
                                    'employee_id': promo.id,
                                    'type_fonction_id': promo.nature_travail_id.id,
                                    'job_id': promo.job_id.id,
                                    'duree': promo.job_id.id,
                                    'date_promotion': self.date_promotion,
                                    'grade_id': promo.grade_id.id,
                                    'categorie_id': promo.categorie_id.id,
                                    'date_grade': promo.date_grade,
                                    'grade_new_id': promo.grade_id.id,
                                    'date_new_grade': relativedelta(months=int(self.duree_promotion) * 12) + fields.Date.from_string(promo.date_grade),
                                    'duree': int(self.duree_promotion) * 12,
                                    'sauvegarde': self.sauvegarde,
                                    'retenue': self.sauvegarde
                                })


            return {
                'name': 'Droit Promotion',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.promotion.droit',
                'type': 'ir.actions.act_window',
                'domain': [('date_promotion', '=', self.date_promotion),('valider', '=', False)]

            }
        else:
            return {
                'name': 'Droit Promotion',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.promotion.droit',
                'type': 'ir.actions.act_window',
                'domain': [('sauvegarde', '=', True)]

            }








