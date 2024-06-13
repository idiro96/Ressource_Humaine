# -*- coding: utf-8 -*-
import babel.dates
from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import UserError
from xlsxwriter import worksheet


class RHDroitPromotion(models.TransientModel):
    _name = 'droit.promotion'


    date_promotion = fields.Date()
    code = fields.Char()
    duree_promotion = fields.Selection([('5', '5'),
                              ('7', '7'),('10', '10'),],
                             readonly=False)
    boul = fields.Boolean(default=False)
    sauvegarde = fields.Boolean(default=False)
    grade_id = fields.Many2one('rh.grade')

    def print_report(self):
        return self.env.ref('ressource_humaine.liste_promotions').report_action(self)

    def export_report(self):
        return self.env.ref('ressource_humaine.action_droit_promotions_xlsx').report_action(self)

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
            grille = self.env['rh.grille'].search(
                [], limit=1, order='create_date DESC')
            for gril in grille:
                print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee')
                categ = self.env['rh.categorie'].search(
                    [('intitule', '=', '14'), ('grille_id', '=', gril.id),
                     ('type_fonction_id', '=', nature_travail.id)])
                categ2 = self.env['rh.categorie'].search(
                    [('intitule', '=', 'ب'), ('grille_id', '=', gril.id),
                     ('type_fonction_id', '=', nature_travail_superieure.id)])
                if categ2:
                    for cat in categ2:
                        section2 = self.env['rh.section'].search(
                            [('categorie_id', '=', cat.id), ('intitule', '=', '2')])
                if categ:
                    for record in categ:
                        indice = record.Indice_minimal
                        print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee1')
            tab = []
            if self.grade_id:
                grade_line = self.env['rh.grade.line'].search(
                    [('grade_id', '=', self.grade_id.id)])
                print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee2')
                if grade_line:
                    for gradeline in grade_line:
                        print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee3')
                        employe = self.env['hr.employee'].search([('grade_id', '=', gradeline.grade2_id.id)])
                        print('gradeline')
                        print(gradeline)
                        if self.duree_promotion == '5':
                            promotion_line1 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', self.date_promotion),('grade_id', '=', gradeline.grade2_id.id),('categorie_grade_indice', '<', indice),('nature_travail_id', '=', nature_travail.id),('fin_relation', '=', False)],
                                    order='date_grade DESC')
                            print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee4')
                            print(promotion_line1)
                        elif self.duree_promotion == '7':
                            promotion_line1 = self.env['hr.employee'].search(
                                [('date_grade', '<=', self.date_promotion),('grade_id', '=', gradeline.grade2_id.id), ('categorie_grade_indice', '>=', indice),('nature_travail_id', '=', nature_travail.id),('fin_relation', '=', False)],
                                order='date_grade DESC')
                            print('>821')
                        else:
                            dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                            promotion_line1 = self.env['hr.employee'].search(
                                [('date_grade', '<=', dateDebut_object10),('grade_id', '=', gradeline.grade2_id.id),('fin_relation', '=', False),('nature_travail_id', '=', nature_travail.id),('promotion_dix', '=', False)],
                                order='date_grade DESC')
                            print('+10')
                        tab.append(promotion_line1)
                        if self.duree_promotion == '5':
                            promotion_line2 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', self.date_promotion),('grade_id', '=', gradeline.grade2_id.id),('categorie_grade_indice', '<', indice),('nature_travail_id', '=', nature_travail_superieure.id),('fin_relation', '=', False)],
                                    order='date_grade DESC')
                            print('<821')
                        elif self.duree_promotion == '7':
                            promotion_line2 = self.env['hr.employee'].search(
                                [('date_grade', '<=', self.date_promotion),('grade_id', '=', gradeline.grade2_id.id), ('categorie_grade_indice', '>=', indice),('nature_travail_id', '=', nature_travail_superieure.id),('fin_relation', '=', False)],
                                order='date_grade DESC')
                            print('>821')
                        else:
                            dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                            promotion_line2 = self.env['hr.employee'].search(
                                [('date_grade', '<=', dateDebut_object10),('grade_id', '=', gradeline.grade2_id.id),('fin_relation', '=', False),('nature_travail_id', '=', nature_travail_superieure.id),('promotion_dix', '=', False)],
                                order='date_grade DESC')
                        tab.append(promotion_line2)
            else:
                if self.duree_promotion == '5':
                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion), ('categorie_grade_indice', '<', indice),
                         ('nature_travail_id', '=', nature_travail.id), ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('<821')
                elif self.duree_promotion == '7':
                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion), ('categorie_grade_indice', '>=', indice),
                         ('nature_travail_id', '=', nature_travail.id), ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('>821555555555555555555555555555555555555555555555555555555555555555')
                    print(promotion_line1)
                else:
                    dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', dateDebut_object10), ('fin_relation', '=', False),
                         ('nature_travail_id', '=', nature_travail.id), ('promotion_dix', '=', False)],
                        order='date_grade DESC')
                    print('+10')


                tab.append(promotion_line1)
                if self.duree_promotion == '5':
                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion), ('categorie_grade_indice', '<', indice),
                         ('nature_travail_id', '=', nature_travail_superieure.id), ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('<821')
                elif self.duree_promotion == '7':
                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', self.date_promotion), ('categorie_grade_indice', '>=', indice),
                         ('nature_travail_id', '=', nature_travail_superieure.id), ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('>82144444444444444444444444444444444444444444444444444444444444')
                    print(promotion_line2)
                else:
                    dateDebut_object10 = fields.Date.from_string(self.date_promotion) - relativedelta(months=120)
                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', dateDebut_object10), ('fin_relation', '=', False),
                         ('nature_travail_id', '=', nature_travail_superieure.id), ('promotion_dix', '=', False)],
                        order='date_grade DESC')
                tab.append(promotion_line2)

            if  promotion_line1 and promotion_line2:
                promotion_line = promotion_line1 + promotion_line2
            if  promotion_line1 and not promotion_line2:
                promotion_line = promotion_line1
            if  not promotion_line1 and promotion_line2:
                promotion_line = promotion_line2
            promotion_ligne3 = promotion_line
            tab3 = []
            tab3 = tab
            if tab:
                for t in tab:
                    for rec in t:
                        print(rec.name)
                        promotion_ligne2 = self.env['rh.promotion.line'].search(
                        [('employee_id', '=', rec.id), ('date_promotion', '=', self.date_promotion)])
                        if promotion_ligne2:
                            promotion_ligne3 = promotion_ligne3 - rec
                            # if tab3[t]:
                            tab3.remove(t)


            if promotion_ligne3:
                promotion_line = promotion_ligne3
            if tab3:
                tab = tab3

            if tab:
                for t in tab:
                    for promo in t:
                        grade2 = self.env['rh.grade.line'].search(
                            [('grade2_id', '=', promo.grade_id.id)])
                        promotion_ligne_droit2 = self.env['rh.promotion.droit'].search(
                            [('employee_id', '=', promo.id), ('date_promotion', '=', self.date_promotion)])
                        promotion_ligne_droit3 = self.env['rh.promotion.droit'].search(
                            [('employee_id', '=', promo.id), ('sauvegarde', '=', True),('retenue', '=', True)],order='date_grade DESC', limit=1)
                        if not promotion_ligne_droit2:
                            dateDebut_object = fields.Date.from_string(self.date_promotion)
                            dateDebut_object2 = fields.Date.from_string(promo.date_grade)
                            difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                            print(difference)
                            if difference >= int(self.duree_promotion) * 12:
                                if promotion_ligne_droit3:
                                    print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee167')
                                    if fields.Date.from_string(promotion_ligne_droit3.date_new_grade) == fields.Date.from_string(promo.date_grade):
                                        print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee163')
                                        self.env['rh.promotion.droit'].create({
                                            'employee_id': promo.id,
                                            'type_fonction_id': promo.nature_travail_id.id,
                                            'job_id': promo.job_id.id,
                                            'duree': promo.job_id.id,
                                            'date_promotion': self.date_promotion,
                                            'grade_id': promo.grade_id.id,
                                            'categorie_id': promo.categorie_id.id,
                                            'date_grade': promo.date_grade,
                                            'grade_new_id': grade2.grade_id.id,
                                            'date_new_grade': relativedelta(months=int(self.duree_promotion) * 12) + fields.Date.from_string(promo.date_grade),
                                            'duree': int(self.duree_promotion) * 12,
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })
                                    else:
                                        print('employe existe')
                                else:
                                    print('errrrrrrrrrrreeeeeeeeeeeeeeeeeeeeeeee169')
                                    self.env['rh.promotion.droit'].create({
                                        'employee_id': promo.id,
                                        'type_fonction_id': promo.nature_travail_id.id,
                                        'job_id': promo.job_id.id,
                                        'duree': promo.job_id.id,
                                        'date_promotion': self.date_promotion,
                                        'grade_id': promo.grade_id.id,
                                        'categorie_id': promo.categorie_id.id,
                                        'date_grade': promo.date_grade,
                                        'grade_new_id': grade2.grade_id.id,
                                        'date_new_grade': relativedelta(months=int(self.duree_promotion) * 12) + fields.Date.from_string(promo.date_grade),
                                        'duree': int(self.duree_promotion) * 12,
                                        'sauvegarde': self.sauvegarde,
                                        'retenue': self.sauvegarde
                                    })

            if self.grade_id:
                return {
                    'name': 'Droit Promotion',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'rh.promotion.droit',
                    'type': 'ir.actions.act_window',
                    'domain': [('date_promotion', '=', self.date_promotion),('grade_new_id', '=', self.grade_id.id),('valider', '=', False)]

                }
            else:
                return {
                    'name': 'Droit Promotion',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'rh.promotion.droit',
                    'type': 'ir.actions.act_window',
                    'domain': [('date_promotion', '=', self.date_promotion), ('valider', '=', False)]

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


class listePromotionReport(models.AbstractModel):
        _name = 'report.ressource_humaine.liste_promotions_report'

        date_promotion_wizard = fields.Date()
        duree_promotion = fields.Integer()
        duree1 = fields.Integer()
        bool = fields.Boolean(default=False)
        time_years = fields.Integer()
        time_months = fields.Integer()
        time_days = fields.Integer()
        time_difference = fields.Char()
        indice = fields.Integer()
        indice2 = fields.Integer()
        indice3 = fields.Integer()

        @api.model
        def get_report_values(self, docids, data=None):
            duree1 = 0
            promotion_line1 = None
            promotion_line2 = None
            promotion_line = None
            # print('self.date_promotion_')
            # print(self.date_avancement)
            params = self.env['droit.promotion'].search([])
            promotion = self.env['droit.promotion'].browse(docids[0])
            date_promotion_wizard = promotion.date_promotion
            formatted_date_promotion_wizard = datetime.strptime(date_promotion_wizard, "%Y-%m-%d").strftime("%Y")
            nature_travail = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonction')])
            nature_travail_superieure = self.env['rh.type.fonction'].search(
                [('code_type_fonction', '=', 'fonctionsuperieure')])

            grille = self.env['rh.grille'].search(
                [],limit=1, order='create_date DESC')
            for gril in grille:
                categ = self.env['rh.categorie'].search(
                    [('intitule', '=', '14'),('grille_id', '=', gril.id),('type_fonction_id', '=', nature_travail.id)])
                categ2 = self.env['rh.categorie'].search(
                    [('intitule', '=', 'ب'), ('grille_id', '=', gril.id),
                     ('type_fonction_id', '=', nature_travail_superieure.id)])
                if categ2:
                    for cat in categ2:
                        section2 = self.env['rh.section'].search(
                            [('categorie_id', '=', cat.id),('intitule', '=', '2')])

            for rec in params:
                date_promotion_wizard = rec.date_promotion
                duree_promotion = rec.duree_promotion
                grade = rec.grade_id
                formatted_date_promotion = datetime.strptime(date_promotion_wizard, "%Y-%m-%d").strftime("%Y")
                date_promotion_wizard2 = fields.Date.from_string(
                        date_promotion_wizard) - relativedelta(months=int(duree_promotion) * 12)
                bool = rec.boul
                if categ:
                    for record in categ:
                        indice = record.Indice_minimal
                if section2:
                    for record in section2:
                        indice2 = record.indice_base
            print('indice')
            print(indice)
            print('indice2')
            print(indice2)

            tab = []
            if grade:
                grade_line = self.env['rh.grade.line'].search(
                    [('grade_id', '=', grade.id)])
                if grade_line:
                    for gradeline in grade_line:
                        employe = self.env['hr.employee'].search([('grade_id', '=', gradeline.grade2_id.id)])
                        print('gradeline')
                        print(gradeline)
                        for rec in employe:
                            print('rec')
                            print(rec)
                            if duree_promotion == '5':
                                promotion_line1 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('categorie_grade_indice', '<', indice),('id', '=', rec.id), ('nature_travail_id', '=', nature_travail.id),
                                     ('fin_relation', '=', False)],
                                    order='date_grade DESC')

                            elif duree_promotion == '7':
                                promotion_line1 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('categorie_grade_indice', '>=', indice), ('nature_travail_id', '=', nature_travail.id),('id', '=', rec.id),
                                     ('fin_relation', '=', False)],
                                    order='date_grade DESC')

                            else:

                                promotion_line1 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail.id),('id', '=', rec.id),
                                     ('promotion_dix', '=', False)],
                                    order='date_grade DESC')
                            tab.append(promotion_line1)
                            if duree_promotion == '5':
                                promotion_line2 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('categorie_grade_indice', '<', indice),('nature_travail_id', '=', nature_travail_superieure.id),('id', '=', rec.id),
                                     ('fin_relation', '=', False)],
                                    order='date_grade DESC')
                                print('<821')
                            elif duree_promotion == '7':
                                promotion_line2 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('categorie_grade_indice', '>=', indice), ('nature_travail_id', '=', nature_travail_superieure.id),('id', '=', rec.id),
                                     ('fin_relation', '=', False)],
                                    order='date_grade DESC')

                            else:

                                promotion_line2 = self.env['hr.employee'].search(
                                    [('date_grade', '<=', date_promotion_wizard),
                                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail_superieure.id),('id', '=', rec.id),
                                     ('promotion_dix', '=', False)],
                                    order='date_grade DESC')
                            tab.append(promotion_line2)

            else:
                if duree_promotion == '5':
                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('categorie_grade_indice', '<', indice), ('nature_travail_id', '=', nature_travail.id),
                         ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    # print('<821')
                elif duree_promotion == '7':
                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('categorie_grade_indice', '>=', indice), ('nature_travail_id', '=', nature_travail.id),
                         ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('>8212222222222222211111111111111111111111111111111111111111111111111111')
                    # print('>821')
                else:

                    promotion_line1 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail.id),
                         ('promotion_dix', '=', False)],
                        order='date_grade DESC')
                tab.append(promotion_line1)
                if duree_promotion == '5':
                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('categorie_grade_indice', '<', indice),('nature_travail_id', '=', nature_travail_superieure.id),
                         ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    # print('<821')
                elif duree_promotion == '7':
                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('categorie_grade_indice', '>=', indice), ('nature_travail_id', '=', nature_travail_superieure.id),
                         ('fin_relation', '=', False)],
                        order='date_grade DESC')
                    print('>8212222222222222222222222222222222222222222222222222222222222222222')
                else:

                    promotion_line2 = self.env['hr.employee'].search(
                        [('date_grade', '<=', date_promotion_wizard),
                         ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail_superieure.id),
                         ('promotion_dix', '=', False)],
                        order='date_grade DESC')
                tab.append(promotion_line2)
            promotions = []
            if  promotion_line1 and promotion_line2:
                promotion_line = promotion_line1 + promotion_line2
            if  promotion_line1 and not promotion_line2:
                promotion_line = promotion_line1
            if  not promotion_line1 and promotion_line2:
                promotion_line = promotion_line2

            print('promotions[] avant append :', promotion_line)
            if promotion_line:
                for empl in promotion_line:
                    # print('date_promotion_wizard')
                    # print(date_promotion_wizard)
                    # print('empl.date_promotion_wizard')
                    # print(empl.date_grade)
                    duree = []

            if tab:
                for t in tab:
                    for empl in t:
                        print('date_promotion_wizard')
                        print(date_promotion_wizard)
                        print('empl.date_promotion_wizard')
                        print(empl.date_grade)
                        duree = []

                        if empl.date_grade:
                            dateDebut_object = fields.Date.from_string(date_promotion_wizard)
                            dateDebut_object2 = fields.Date.from_string(empl.date_grade)
                            difference = (
                                                     dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month

                            if difference >= int(duree_promotion) * 12:
                                promotions.append(empl)

                                duree1 = int(duree_promotion) * 12

            print('promotions[] aprés append :', promotions)
            line_date_new_promotion_av = {}
            for rec in promotions:
                for rec2 in rec:
                    if rec2.date_grade:

                        date_new_promotion_av_str = relativedelta(months=int(duree_promotion) * 12) + fields.Date.from_string(
                                rec2.date_grade)

                        if date_new_promotion_av_str:

                            # formatted_date_new_avancement_av = datetime.strptime(date_new_avancement_av_str, "%Y-%m-%d").strftime(
                            #                 "%d-%m-%Y")
                            line_date_new_promotion_av[rec2.id] = date_new_promotion_av_str
            line_date_new_promotion_av2 = {}
            for rec in promotions:
                for rec2 in rec:
                    if rec2.date_grade:
                        date_new_promotion = fields.Datetime.from_string(date_promotion_wizard)


                        date_old_promotion = fields.Date.from_string(
                            rec2.date_grade)

                        print(date_new_promotion)

                        # print('date_new_avancement2')
                        # print(date_new_promotion)
                        delta = relativedelta(date_new_promotion, date_old_promotion)

                        years = delta.years
                        months = delta.months
                        days = delta.days

                        time_years = years
                        time_months = months
                        time_days = days
                        time_difference = f"قدره {years} سنة و {months} شهر و {days} يوم"
                        # print('time_difference')
                        # print(time_difference)
                        line_date_new_promotion_av2[rec2.id] = time_difference
            line_grade = {}
            for rec in promotions:
                for rec2 in rec:
                        if rec2.grade_id:
                            promotion2 = self.env['rh.grade.line'].search(
                                [('grade2_id', '=', rec2.grade_id.id)])
                            for prom in promotion2:
                                line_grade[rec2.id] = prom.grade_id.intitule_grade

            report_data = {
                'employee_droit': promotions,
                'duree1': duree1,
                'line_date_new_promotion_av': line_date_new_promotion_av,
                'line_date_new_promotion_av2': line_date_new_promotion_av2,
                'line_grade': line_grade,
                'date': formatted_date_promotion,
                'date': formatted_date_promotion_wizard,
            }

            return report_data


class DroitPromotiondXLS(models.AbstractModel):
    _name = 'report.ressource_humaine.droit_promotions_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        promotion = self._get_objs_for_report(objs.ids, data)
        date_promotion = promotion.date_promotion
        formatted_date_promotion = datetime.strptime(date_promotion, "%Y-%m-%d").strftime("%Y")
        duree1 = 0
        promotion_line1 = None
        promotion_line2 = None
        promotion_line = None
        params = self.env['droit.promotion'].search([])
        nature_travail = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonction')])
        nature_travail_superieure = self.env['rh.type.fonction'].search([('code_type_fonction', '=', 'fonctionsuperieure')])

        for rec in params:
            date_promotion_wizard = rec.date_promotion
            duree_promotion = rec.duree_promotion
            grade = rec.grade_id
            date_promotion_wizard2 = fields.Date.from_string(date_promotion_wizard) - relativedelta(months=int(duree_promotion) * 12)
            bool = rec.boul

        if grade:
            if duree_promotion == '5':
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('indice_minimal', '<', 821), ('grade_id', '=', grade.id),
                     ('nature_travail_id', '=', nature_travail.id), ('grade_id', '=', grade.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            elif duree_promotion == '7':
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('indice_minimal', '>=', 821), ('nature_travail_id', '=', nature_travail.id),
                     ('grade_id', '=', grade.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            else:
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail.id),
                     ('grade_id', '=', grade.id),
                     ('promotion_dix', '=', False)],
                    order='date_grade DESC')
            if duree_promotion == '5':
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('point_indiciare', '<', 4103), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('grade_id', '=', grade.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            elif duree_promotion == '7':
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('point_indiciare', '>=', 4103), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('grade_id', '=', grade.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            else:
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('grade_id', '=', grade.id),
                     ('promotion_dix', '=', False)],
                    order='date_grade DESC')

        else:
            if duree_promotion == '5':
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('indice_minimal', '<', 821), ('nature_travail_id', '=', nature_travail.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            elif duree_promotion == '7':
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('indice_minimal', '>=', 821), ('nature_travail_id', '=', nature_travail.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            else:
                promotion_line1 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail.id),
                     ('promotion_dix', '=', False)],
                    order='date_grade DESC')
            if duree_promotion == '5':
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('point_indiciare', '<', 4103), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            elif duree_promotion == '7':
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('point_indiciare', '>=', 4103), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('fin_relation', '=', False)],
                    order='date_grade DESC')
            else:
                promotion_line2 = self.env['hr.employee'].search(
                    [('date_grade', '<=', date_promotion_wizard),
                     ('fin_relation', '=', False), ('nature_travail_id', '=', nature_travail_superieure.id),
                     ('promotion_dix', '=', False)],
                    order='date_grade DESC')

        promotions = []
        if promotion_line1 and promotion_line2:
            promotion_line = promotion_line1 + promotion_line2
        if promotion_line1 and not promotion_line2:
            promotion_line = promotion_line1
        if not promotion_line1 and promotion_line2:
            promotion_line = promotion_line2

        for empl in promotion_line:
            duree = []
            if empl.date_grade:
                datedebut_object = fields.Date.from_string(date_promotion_wizard)
                datedebut_object2 = fields.Date.from_string(empl.date_grade)
                difference = (datedebut_object.year - datedebut_object2.year) * 12 + datedebut_object.month - datedebut_object2.month
                if difference >= int(duree_promotion) * 12:
                    promotions.append(empl)
                    duree1 = int(duree_promotion) * 12

        line_date_new_promotion_av = {}
        for rec in promotions:
            for rec2 in rec:
                if rec2.date_grade:
                    date_new_promotion_av_str = relativedelta(months=int(duree_promotion) * 12) + fields.Date.from_string(rec2.date_grade)
                    if date_new_promotion_av_str:
                        line_date_new_promotion_av[rec2.id] = date_new_promotion_av_str

        line_date_new_promotion_av2 = {}
        for rec in promotions:
            for rec2 in rec:
                if rec2.date_grade:
                    date_new_promotion = fields.Datetime.from_string(date_promotion_wizard)
                    date_old_promotion = fields.Date.from_string(rec2.date_grade)
                    delta = relativedelta(date_new_promotion, date_old_promotion)
                    years = delta.years
                    months = delta.months
                    days = delta.days
                    time_years = years
                    time_months = months
                    time_days = days
                    time_difference = f"قدره {years} سنة و {months} شهر و {days} يوم"
                    line_date_new_promotion_av2[rec2.id] = time_difference

        format1 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format1.set_text_wrap()
        format1.set_align('center')
        format1.set_valign('vcenter')
        format2 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format2.set_text_wrap()
        format2.set_align('center')
        format2.set_valign('vcenter')
        format3 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#FFFFFF'})
        date_format = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                                           'bg_color': '#FFFFFF', 'num_format': 'J MMMM AAAA'})
        date_format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                                           'bg_color': '#FFFFFF', 'num_format': 'AAAA - MM - JJ'})
        title_format = workbook.add_format(
            {'bold': True, 'font_size': 32, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#FFFFFF'})
        sheet = workbook.add_worksheet('جدول ترقية')
        sheet.right_to_left()

        sheet.set_row(6, 25)
        for row_num in range(7, len(promotions) + 1):
            sheet.set_row(row_num, 20)

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 10)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 10)
        sheet.set_column(7, 7, 25)
        sheet.set_column(8, 8, 25)
        sheet.set_column(9, 9, 10)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 25)
        sheet.set_column(13, 13, 30)

        sheet.write(6, 0, 'الرقم', format1)
        sheet.write(6, 1, 'الاسم و اللقب', format1)
        sheet.write(6, 2, 'تاريخ الميلاد', format1)
        sheet.write(6, 3, 'الحالة العائلية', format1)
        sheet.write(6, 4, 'الرتبة', format1)
        sheet.write(6, 5, 'المنصب', format1)
        sheet.write(6, 6, 'الدرجة', format1)
        sheet.write(6, 7, 'تاريخ سريان الترقيةالحالية', format1)
        sheet.write(6, 8, 'ترقية', format1)
        sheet.write(6, 9, 'عامين و نصف', format1)
        sheet.write(6, 10, 'المدة', format1)
        sheet.write(6, 11, 'التنقيط', format1)
        sheet.write(6, 12, 'تاريخ سريان الترقية القادمة', format1)
        sheet.write(6, 13, 'فرق المدة', format1)

        sheet.merge_range('E2:J4', f"{formatted_date_promotion}جدول ترقية موظفي المدرسة الوطنية للإدارة لسنة ",
                          title_format)

        row = 7
        for index, line in enumerate(promotions, start=1):
            sheet.write(row, 0, index, format2)
            sheet.write(row, 1, line.name, format3)
            sheet.write(row, 2, line.birthday, format3)
            if line.marital == 'single':
                if line.gender == 'male':
                    sheet.write(row, 3, 'أعزب', format3)
                elif line.gender == 'female':
                    sheet.write(row, 3, 'عازبة', format3)
                else:
                    sheet.write(row, 3, 'أعزب', format3)
            elif line.marital == 'married':
                if line.gender == 'male':
                    sheet.write(row, 3, 'متزوّج', format3)
                elif line.gender == 'female':
                    sheet.write(row, 3, 'متزوّجة', format3)
                else:
                    sheet.write(row, 3, 'متزوّج', format3)
            elif line.marital == 'widower':
                if line.gender == 'male':
                    sheet.write(row, 3, 'أرمل', format3)
                elif line.gender == 'female':
                    sheet.write(row, 3, 'أرملة', format3)
                else:
                    sheet.write(row, 3, 'أرمل', format3)
            elif line.marital == 'divorced':
                if line.gender == 'male':
                    sheet.write(row, 3, 'مطلّق', format3)
                elif line.gender == 'female':
                    sheet.write(row, 3, 'مطلّقة', format3)
                else:
                    sheet.write(row, 3, 'مطلّق', format3)
            else:
                sheet.write(row, 3, '/', format3)
            sheet.write(row, 4, line.grade_id.intitule_grade or '/', format3)
            sheet.write(row, 5, line.job_id.name or '/', format3)
            sheet.write(row, 6, line.echelon_id.intitule or '/', format3)
            sheet.write(row, 7, line.date_grade or '/', format3)
            date_str = line.date_grade
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                sheet.write(row, 8, date_obj, date_format)
            else:
                sheet.write(row, 8, '/', format3)
            sheet.write(row, 9, duree1 or '/', format3)
            sheet.write(row, 10, '', format3)
            sheet.write(row, 11, '', format3)
            sheet.write(row, 12, line_date_new_promotion_av.get(line.id, '') or '/', date_format2)
            sheet.write(row, 13, line_date_new_promotion_av2.get(line.id, '') or '/', format3)
            row += 1

