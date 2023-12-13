# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _



class HrEmployeInherited(models.Model):
    _inherit = "hr.employee"


    handicape = fields.Boolean(default=False)
    service_militaire = fields.Boolean(default=False)
    fin_relation = fields.Boolean(default=False)
    date_fin_relation = fields.Date()
    date_entrer = fields.Date()
    date_reintegration = fields.Date()
    activite_conjoint = fields.Boolean(default=False)
    visite_medical_detaille_id = fields.Many2one('ressource_humaine.visite.medical.detaille')
    formation_detail_id = fields.Many2one('ressource_humaine.formation.detail')
    selection_employe_visite_medicale = fields.Boolean('Sélection', default=False)
    days_off = fields.Float(compute='_compute_days_off', string='Total Days Off', store=True)


    @api.depends('date_entrer')
    def _compute_days_off(self):
        for employee in self:
            if employee.date_entrer:
                # Assuming date_entry is a Date field in the hr.employee model
                entrer_date = fields.Date.from_string(employee.date_entrer)
                #
                # dateDebut_object = fields.Date.from_string(entrer_date)
                #
                # jour = datetime.strptime(entrer_date, '%Y-%m-%d').day
                # mois = datetime.strptime(entrer_date, '%Y-%m-%d').month
                # year = datetime.strptime(entrer_date, '%Y-%m-%d').year
                #
                # days_off = days_off + 2.5
                #
                # debut_annee = date(dateDebut_object.year, mois, 1)
                # debut_fin = relativedelta(months=0) + debut_annee
                # print(debut_annee)
                # print(debut_fin)

                today_date = fields.Date.from_string(fields.Date.today())
                months_passed = (today_date.year - entrer_date.year) * 12 + today_date.month - entrer_date.month
                days_off = months_passed * 2.5
                employee.days_off = days_off








    
