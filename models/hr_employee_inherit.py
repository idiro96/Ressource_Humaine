# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging
import calendar
import time


class HrEmployeInherited(models.Model):
    _inherit = "hr.employee"


    handicape = fields.Boolean(default=False)
    service_militaire = fields.Boolean(default=False)
    fin_relation = fields.Boolean(default=False)
    date_fin_relation = fields.Date()
    date_debut_emploi = fields.Date()
    numero_identif_national = fields.Char()
    prenom_pere = fields.Char()
    nom_mere = fields.Char()
    prenom_mere = fields.Char()
    date_entrer = fields.Date()
    date_reintegration = fields.Date()
    activite_conjoint = fields.Boolean(default=False)
    visite_medical_detaille_id = fields.Many2one('ressource_humaine.visite.medical.detaille')
    formation_detail_id = fields.Many2one('ressource_humaine.formation.detail')

    selection_employe = fields.Boolean('Sélection', default=False)
    days_off = fields.Float(compute='_compute_days_off', string='Total Days Off', store=True)
    corps_id = fields.Many2one('rh.corps')
    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='employee_id', string="Promotion Lines")
    nature_travail_id = fields.Many2one('rh.nature.travail')
    position_statutaire = fields.Selection([('activite', 'القيام بالخدمة'),
                              ('detachement', 'الانتداب'),
                              ('horscadre', 'خارج الايطار '),('miseendisponibilite', 'الاحالة على الاستدعاء '),('servicenationale', 'الخدمة الوطنية'),],
                               string="Status", readonly=False,default='activite')
    nature_handicap = fields.Selection([('audio', 'سمعي'),
                              ('visuel', 'بصري'),
                              ('cinetique', 'حركي')],
                              readonly=False,default='audio')
    taux_handicap = fields.Float()
    corps_visible = fields.Boolean(default=True)


    @api.depends('date_entrer')
    def _compute_days_off(self):
        for employee in self:
            if employee.date_entrer:
                # Assuming date_entry is a Date field in the hr.employee model
                # entrer_date = fields.Date.from_string(employee.date_entrer)
                # today_date = fields.Date.from_string(fields.Date.today())
                # months_passed = (today_date.year - entrer_date.year) * 12 + today_date.month - entrer_date.month
                # days_off = months_passed * 2.5
                days_off = 0
                conge_existe = self.env['rh.congedroit'].search(
                        [('id_personnel', '=', employee.id)])
                for conge in conge_existe:
                    days_off = conge.nbr_jour_reste + days_off

                employee.days_off = days_off

    @api.onchange('nature_travail_id')
    def _onchange_related_field_filier(self):
        print('teste')
        for rec in self:
            domain = []
            if rec.nature_travail_id:
                if rec.nature_travail_id == 'المتعاقدين':
                    corps_visible = False
                else:
                    corps_visible = True
                print('teste')
                jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                print(jobs)
                domain.append(('id', 'in', jobs.ids))
            else:
                domain = ''

        res = {'domain': {'job_id': domain}}
        print(res)
        return res





    
