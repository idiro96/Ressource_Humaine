# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar
from odoo.exceptions import ValidationError


class RHDroitAvencement(models.TransientModel):
    _name = 'droit.avencement'


    date_avancement = fields.Date()
    code = fields.Char()
    boul = fields.Boolean(default=False)
    reclassement = fields.Boolean(default=False)
    sauvegarde = fields.Boolean(default=False)
    grade_id = fields.Many2one('rh.grade')

    @api.multi
    def Archiver(self):
        print('glllllllllll')
        self.sauvegarde = True

    def print_report(self):
        return self.env.ref('ressource_humaine.liste_avancements').report_action(self)


    def check_avancement_date_and_sauvegarde(self):
        for wizard_record in self:
            # Check if there is a corresponding record in RHAvencementDroit with sauvegarde=True
            avencement_droit_record = self.env['rh.avencement.droit'].search([
                ('date_avancement', '=', wizard_record.date_avancement),
                ('code', '=', wizard_record.code),  # Assuming code is a field in RHAvencementDroit
                ('sauvegarde', '=', True),
            ])
            if not avencement_droit_record:
                raise ValidationError(
                    "No corresponding RHAvencementDroit record found for the given date_avancement, code, and sauvegarde=True.")

    @api.multi
    def actualiser_droit_avencement(self):
        if self.boul == False:
            avancement_ligne_droit = self.env['rh.avencement.droit'].search([])
            for record in avancement_ligne_droit:
                if record.sauvegarde == False:
                    record.unlink()
            if self.grade_id:
                avancement_line = self.env['hr.employee'].search(
                        [('date_avancement', '<=', self.date_avancement),('grade_id', '=', self.grade_id.id),('fin_relation', '=', False)],
                        order='date_avancement DESC')
            else:
                avancement_line = self.env['hr.employee'].search(
                    [('date_avancement', '<=', self.date_avancement), ('fin_relation', '=', False)],
                    order='date_avancement DESC')

            if avancement_line:
                for avance in avancement_line:
                        avancement_ligne_droit2 = self.env['rh.avencement.droit'].search([('employee_id', '=', avance.id),('date_avancement', '=', self.date_avancement)])
                        avancement_ligne_droit3 = self.env['rh.avencement.droit'].search(
                            [('employee_id', '=', avance.id), ('sauvegarde', '=', True), ('retenue', '=', True)], order='date_avancement DESC', limit=1)
                        if not avancement_ligne_droit2:
                            dateDebut_object = fields.Date.from_string(self.date_avancement)
                            dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                            difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                            if self.reclassement == False:
                                if difference >= 30 and avance.nature_travail_id.code_type_fonction == 'fonction':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                                avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'groupe_old_id': avance.groupe_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'echelon_old_id': avance.echelon_id.id,

                                                'grille_new_id': avance.grille_id.id,
                                                'groupe_new_id': avance.groupe_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 30,
                                                'duree_lettre': 'superieure',
                                                'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                                })

                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'groupe_old_id': avance.groupe_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'groupe_new_id': avance.groupe_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 30,
                                            'duree_lettre': 'superieure',
                                            'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })

                                elif difference >= 30 and avance.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                            avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'section_old_id': avance.section_id.id,
                                                'echelon_old_id': avance.echelon_id.id,
                                                'grille_new_id': avance.grille_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'section_new_id': avance.section_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 30,
                                                'duree_lettre': 'inferieure',
                                                'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                                })
                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'section_old_id': avance.section_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'section_new_id': avance.section_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 30,
                                            'duree_lettre': 'inferieure',
                                            'date_new_avancement': relativedelta(months=30) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })

                                elif difference >= 30 and avance.nature_travail_id.code_type_fonction == 'postesuperieure':
                                     print('fff')


                            else:
                                if difference >= 24 and avance.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                                    if avancement_ligne_droit3:
                                        if fields.Date.from_string(
                                                avancement_ligne_droit3.date_new_avancement) == fields.Date.from_string(
                                            avance.date_avancement):
                                            self.env['rh.avencement.droit'].create({
                                                'employee_id': avance.id,
                                                'type_fonction_id': avance.nature_travail_id.id,
                                                'date_avancement': self.date_avancement,
                                                'date_old_avancement': avance.date_avancement,
                                                'grade_id': avance.grade_id.id,
                                                'job_id': avance.job_id.id,
                                                'grille_old_id': avance.grille_id.id,
                                                'categorie_old_id': avance.categorie_id.id,
                                                'section_old_id': avance.section_id.id,
                                                'echelon_old_id': avance.echelon_id.id,
                                                'grille_new_id': avance.grille_id.id,
                                                'categorie_new_id': avance.categorie_id.id,
                                                'section_new_id': avance.section_id.id,
                                                'echelon_new_id': avance.echelon_id.id,
                                                'duree': 24,
                                                'duree_lettre': 'inferieure',
                                                'date_new_avancement': relativedelta(months=24) + fields.Date.from_string(
                                                    avance.date_avancement),
                                                'sauvegarde': self.sauvegarde,
                                                'retenue': self.sauvegarde
                                            })
                                        else:
                                            print('employe existe')
                                    else:
                                        self.env['rh.avencement.droit'].create({
                                            'employee_id': avance.id,
                                            'type_fonction_id': avance.nature_travail_id.id,
                                            'date_avancement': self.date_avancement,
                                            'date_old_avancement': avance.date_avancement,
                                            'grade_id': avance.grade_id.id,
                                            'job_id': avance.job_id.id,
                                            'grille_old_id': avance.grille_id.id,
                                            'categorie_old_id': avance.categorie_id.id,
                                            'section_old_id': avance.section_id.id,
                                            'echelon_old_id': avance.echelon_id.id,
                                            'grille_new_id': avance.grille_id.id,
                                            'categorie_new_id': avance.categorie_id.id,
                                            'section_new_id': avance.section_id.id,
                                            'echelon_new_id': avance.echelon_id.id,
                                            'duree': 24,
                                            'duree_lettre': 'inferieure',
                                            'date_new_avancement': relativedelta(months=24) + fields.Date.from_string(
                                                avance.date_avancement),
                                            'sauvegarde': self.sauvegarde,
                                            'retenue': self.sauvegarde
                                        })
            if self.grade_id:
                return {
                    'name': 'Droit Avancement',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'rh.avencement.droit',
                    'type': 'ir.actions.act_window',
                    'domain': [('date_avancement', '=', self.date_avancement),('grade_id', '=', self.grade_id.id),('valider', '=', False)]

                }
            else:
                return {
                    'name': 'Droit Avancement',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'rh.avencement.droit',
                    'type': 'ir.actions.act_window',
                    'domain': [('date_avancement', '=', self.date_avancement), ('valider', '=', False)]

                }
        else:
            return {
                'name': 'Droit Avancement',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'rh.avencement.droit',
                'type': 'ir.actions.act_window',
                'domain': [('sauvegarde', '=', True)]

            }


class listeAvancementReport(models.AbstractModel):
        _name = 'report.ressource_humaine.liste_avancements_report'

        date_avancement_wizard = fields.Date()
        duree1 = fields.Integer()
        bool = fields.Boolean(default=False)
        time_years = fields.Integer()
        time_months = fields.Integer()
        time_days = fields.Integer()
        time_difference = fields.Char()

        @api.model
        def get_report_values(self, docids, data=None):
            duree1 = 0
            print('self.date_avancement')
            # print(self.date_avancement)
            params = self.env['droit.avencement'].search([])
            avancement = self.env['droit.avencement'].browse(docids[0])
            date_avancement_wizard = avancement.date_avancement
            formatted_date_avancement_wizard = datetime.strptime(date_avancement_wizard, "%Y-%m-%d").strftime("%Y")

            for rec in params:
                date_avancement_wizard = rec.date_avancement
                bool = rec.reclassement
                formatted_date_avancement = datetime.strptime(date_avancement_wizard, "%Y-%m-%d").strftime("%Y")
                if not bool:
                    date_avancement_wizard2 = fields.Date.from_string(
                                                    date_avancement_wizard) - relativedelta(months=30)
                else:
                    date_avancement_wizard2 = fields.Date.from_string(
                        date_avancement_wizard) - relativedelta(months=24)

                grade = rec.grade_id

            if grade:
                employees = self.env['hr.employee'].search(
                    [('date_avancement', '<=', date_avancement_wizard2),('grade_id', '=', grade.id),('fin_relation', '=', False)])
            else:
                employees = self.env['hr.employee'].search(
                    [('date_avancement', '<=', date_avancement_wizard2), ('fin_relation', '=', False)])

            avancements = []
            for empl in employees:
                print('date_avancement_wizard')
                print(date_avancement_wizard)
                print('empl.date_avancement_wizard')
                print(empl.date_avancement)
                duree = []

                if empl.date_avancement:
                    dateDebut_object = fields.Date.from_string(date_avancement_wizard)
                    dateDebut_object2 = fields.Date.from_string(empl.date_avancement)
                    difference = (dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    if not bool:
                        if (difference >= 30 and empl.nature_travail_id.code_type_fonction == 'fonction') or (difference >= 30 and empl.nature_travail_id.code_type_fonction == 'fonctionsuperieure'):
                            avancements.append(empl)

                        duree1 = 30
                    else:
                        if (difference >= 24 and empl.nature_travail_id.code_type_fonction == 'fonctionsuperieure'):
                            avancements.append(empl)

                        duree1 = 24

            line_date_new_avancement_av = {}
            for rec in avancements:
                for rec2 in rec:
                    if rec2.date_avancement:
                        print('date_new_avancement_av_str')
                        print(rec2.date_avancement)
                        if not bool:
                            date_new_avancement_av_str = relativedelta(months=30) + fields.Date.from_string(
                                                        rec2.date_avancement)
                        else:
                            date_new_avancement_av_str = relativedelta(months=24) + fields.Date.from_string(
                                rec2.date_avancement)
                        if date_new_avancement_av_str:
                            print('date_new_avancement_av_str2')
                            print(date_new_avancement_av_str)
                            # formatted_date_new_avancement_av = datetime.strptime(date_new_avancement_av_str, "%Y-%m-%d").strftime(
                            #                 "%d-%m-%Y")
                            line_date_new_avancement_av[rec2.id] = date_new_avancement_av_str
            line_date_new_avancement_av2 = {}
            for rec in avancements:
                    for rec2 in rec:
                        if rec2.date_avancement:
                            date_new_avancement = fields.Datetime.from_string(date_avancement_wizard)


                            date_old_avancement = fields.Date.from_string(
                                    rec2.date_avancement)

                            delta = relativedelta(date_new_avancement, date_old_avancement)

                            years = delta.years
                            months = delta.months
                            days = delta.days

                            time_years = years
                            time_months = months
                            time_days = days
                            time_difference = f"قدره {years} سنة و {months} شهر و {days} يوم"
                            print('time_difference')
                            print(time_difference)
                            line_date_new_avancement_av2[rec2.id] = time_difference


            report_data = {
                'employee_droit': avancements,
                'duree1': duree1,
                'line_date_new_avancement_av': line_date_new_avancement_av,
                'line_date_new_avancement_av2': line_date_new_avancement_av2,

                'date': formatted_date_avancement,

                'date': formatted_date_avancement_wizard,
            }

            return report_data








