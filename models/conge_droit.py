# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class RHCongeDroit(models.Model):
    _name = 'rh.congedroit'


    id_personnel = fields.Many2one(comodel_name='hr.employee')
    exercice_conge = fields.Char()
    nbr_jour = fields.Float()
    nbr_jour_consomme = fields.Float()
    nbr_jour_reste = fields.Float()

    @api.model
    def my_function(self):
        (print('testaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') )

    @api.multi
    def Actualiser_Droit_Conge(self):
        liste_emploiyee = self.env['hr.employee'].search([('date_entrer','!=',None)])
        for empl in liste_emploiyee:

            days_off = 0
            current_date = datetime.now().date()
            current_date2 = datetime.now().date()

            entrer_date1 = empl.date_entrer
            print(entrer_date1)
            entrer_date2 = empl.date_entrer
            dateDebut_object = fields.Date.from_string(entrer_date1)
            jour = datetime.strptime(entrer_date1, '%Y-%m-%d').day
            mois = datetime.strptime(entrer_date1, '%Y-%m-%d').month
            year = datetime.strptime(entrer_date1, '%Y-%m-%d').year
            debut_annee = date(dateDebut_object.year, mois, 1)
            year_current = current_date.year
            current_date = dateDebut_object
            while current_date <= current_date2:


                if mois >= 7 and mois <= 12:
                    year = year
                    year_suivant = year + 1
                else:
                        year_suivant = year
                        year = year - 1


                first_date = date(year, 7, 1)
                second_date = date(year_suivant, 6, 30)

                if current_date <=second_date:
                    print('passer')
                    # if mois >= 7 and mois <= 12:
                    #     year = year
                    #     year_suivant = year + 1
                    # else:
                    #     year_suivant = year
                    #     year = year - 1


                else:
                    mois = current_date.month
                    year = current_date.year
                    if mois >= 7 and mois <= 12:
                        year = year
                        year_suivant = year + 1
                    else:
                        year = year - 1
                        year_suivant = year +1


                anne_encours = str(year)  + '/' + str(year_suivant)
                conge_existe = self.env['rh.congedroit'].search(
                        [('exercice_conge', '=', anne_encours), ('id_personnel', '=', empl.id)])
                if conge_existe:
                            print("exercice existe déja")
                            month_now = current_date.month
                            conge_existe_month = self.env['rh.conge_droit_month'].search([('id_conge_droit', '=', conge_existe.id),('month', '=', month_now)])
                            if not conge_existe_month:
                                    days_off = days_off + 2.5
                                    conge_existe.write({'nbr_jour': days_off})
                                    conge_existe.write({'nbr_jour_reste': days_off})
                                    conge_droit_month_new = self.env['rh.conge_droit_month'].create({
                                                        'id_conge_droit': conge_existe.id,
                                                        'month': mois,
                                                    })
                                    print('rabah')
                else:
                    print(current_date)
                    print(entrer_date2)
                    print(jour)
                    if (jour > 15 and (current_date == entrer_date2)):
                        days_off = 0
                        print('iccci1')
                    else:
                        days_off = 2.5
                        print('iccci2')
                    conge_droit2 = self.env['rh.congedroit'].create({
                                        'id_personnel': empl.id,
                                        'exercice_conge': anne_encours,
                                        'nbr_jour': days_off,
                                        'nbr_jour_consomme': 0,
                                        'nbr_jour_reste': days_off,
                                    })

                    conge_droit_month_new = self.env['rh.conge_droit_month'].create({
                        'id_conge_droit': conge_droit2.id,
                        'month': mois,
                    })
                    print('rabah2')

                current_date = relativedelta(months=1) + current_date


                # res = calendar.monthrange(debut_fin.year, debut_fin.month)
                # day = res[1]
                # debut_fin_mois = debut_fin_mois + relativedelta(day=day)
                # print(debut_annee)
                # print(debut_fin)
                # print(debut_fin_mois)
                # months_passed = debut_fin_mois.day - entrer_date1.day
                # print(months_passed)
                #
                # first_date = datetime.date(year, 7, 1)
                # second_date = datetime.date(year_suivant, 6, 30)
                #
                # if current_date <= second_date:
                #         anne_encours = str(year)  + '/' + str(year_suivant)
                #         conge_existe= self.env['rh.congedroit'].search([('exercice_conge', '=', anne_encours),('id_personnel', '=', employee.id)])
                #         if conge_existe:
                #             print("exercice existe déja")
                #             month_now = datetime.strptime(current_date, '%Y-%m-%d').month
                #             conge_existe_month = self.env['rh.conge_droit_month'].search([('month', '=', month_now)])
                #             if not conge_existe_month:
                #                 days_off = days_off + 2.5
                #                 conge_existe.write({'nbr_jour': days_off})
                #         else:
                #             if months_passed >= 15:
                #                 days_off = days_off + 2.5
                #                 conge_droit = self.env['rh.congedroit'].create({
                #                     'id_personnel': employee.id,
                #                     'exercice_conge': anne_encours,
                #                     'nbr_jour': days_off,
                #                     'nbr_jour_consomme': 0,
                #                     'nbr_jour_reste': days_off,
                #                 })
                #                 conge_droit = self.env['rh.conge_droit_month'].create({
                #                     'id_conge_droit': conge_droit.id,
                #                     'month': mois,
                #                 })
                #             else :
                #                 conge_droit = self.env['rh.congedroit'].create({
                #                     'id_personnel': employee.id,
                #                     'exercice_conge': anne_encours,
                #                     'nbr_jour': 0,
                #                     'nbr_jour_consomme': 0,
                #                     'nbr_jour_reste': 0,
                #                 })
                #                 conge_droit = self.env['rh.conge_droit_month'].create({
                #                     'id_conge_droit': conge_droit.id,
                #                     'month': mois,
                #                 })
                #
                #         formatted_date1 = relativedelta(months=1) + debut_annee
                # else :
                #
                #     entrer_date1 = current_date
                #     dateDebut_object = fields.Date.from_string(entrer_date1)
                #     jour = datetime.strptime(entrer_date1, '%Y-%m-%d').day
                #     mois = datetime.strptime(entrer_date1, '%Y-%m-%d').month
                #     year = datetime.strptime(entrer_date1, '%Y-%m-%d').year
                #     year_suivant = year + 1
                #
                #     anne_encours = str(year) + '/' + str(year_suivant)
                #     conge_existe = self.env['rh.congedroit'].search([('exercice_conge', '=', anne_encours),('id_personnel', '=', employee.id)])
                #     if conge_existe:
                #         print("exercice existe déja")
                #         month_now = datetime.strptime(current_date, '%Y-%m-%d').month
                #         conge_existe_month = self.env['rh.conge_droit_month'].search([('month', '=', month_now)])
                #         if not conge_existe_month:
                #             days_off = days_off + 2.5
                #             conge_existe.write({'nbr_jour': days_off})
                #
                #     else:
                #             days_off = days_off + 2.5
                #             conge_droit = self.env['rh.congedroit'].create({
                #                 'id_personnel': employee.id,
                #                 'exercice_conge': anne_encours,
                #                 'nbr_jour': days_off,
                #                 'nbr_jour_consomme': 0,
                #                 'nbr_jour_reste': days_off,
                #             })
                #             conge_droit = self.env['rh.conge_droit_month'].create({
                #                 'id_conge_droit': conge_droit.id,
                #                 'month': mois,
                #             })
                #
                #
                #  # today_date = fields.Date.from_string(fields.Date.today())
                #  # months_passed = (today_date.year - entrer_date.year) * 12 + today_date.month - entrer_date.month
                #  # days_off = months_passed * 2.5
                #  # employee.days_off = days_off
                #
                #










