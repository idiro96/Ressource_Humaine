# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


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



            debut_annee = date(dateDebut_object.year, mois, jour)
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


                # anne_encours = str(year)  + '/' + str(year_suivant)
                anne_encours = str(year)  + '/' + str(year_suivant)
                print(empl.name)
                print(current_date)
                print(anne_encours)
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
                    print(debut_annee)

                    print(jour)
                    if ((jour > 15) and (current_date == debut_annee)):
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

                res = calendar.monthrange(current_date.year, current_date.month)
                day = res[1]
                current_date = current_date + relativedelta(day=day)
                current_date_mois = current_date.month
                current_date_year = current_date.year
                current_date = date(current_date_year, current_date_mois, 15)
                current_date = relativedelta(months=1) + current_date

                print(current_date)
                print('date de mois')
            conge_empl_total = self.env['rh.congedroit'].search(
                [('id_personnel', '=', empl.id)])
            jour_reste = 0
            for cong in conge_empl_total:
                jour_reste = cong.nbr_jour_reste + jour_reste
            empl.write({'days_off': jour_reste})







