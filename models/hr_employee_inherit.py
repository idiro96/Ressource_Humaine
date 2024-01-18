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
    numero_securite_social = fields.Char()
    prenom_pere = fields.Char()
    nom_mere = fields.Char()
    prenom_mere = fields.Char()
    nom_fr = fields.Char()
    prenom_fr = fields.Char()
    date_entrer = fields.Date()
    date_reintegration = fields.Date()
    activite_conjoint = fields.Boolean(default=False)
    visite_medical_detaille_id = fields.Many2one('ressource_humaine.visite.medical.detaille')
    formation_detail_id = fields.Many2one('ressource_humaine.formation.detail')

    selection_employe = fields.Boolean('Sélection', default=False)


    days_off = fields.Float(string='Total Days Off', store=True)

    # days_off = fields.Float(compute='_compute_days_off', store=True, translate=True)

    # days_off = fields.Float(compute='_compute_days_off', store=True, translate=True)
    days_off = fields.Float(store=True)

    corps_id = fields.Many2one('rh.corps')
    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='employee_id')
    avancement_lines = fields.One2many('rh.avancement.line', inverse_name='employee_id')
    nature_travail_id = fields.Many2one('rh.type.fonction')
    position_statutaire = fields.Selection([('activite', 'Activite'),
                              ('detachement', 'Detachement'),
                              ('horscadre', 'Horscadre'),('miseendisponibilite', 'Miseendisponibilite'),('servicenationale', 'Servicenationale'),],
                                readonly=False, default='activite')
    methode_embauche = fields.Selection([('recrutement', 'Recrutement'),
                              ('transfert', 'Transfert'),
                              ('detachement', 'Detachement'),],
                                readonly=False, default='recrutement')
    ancienne_etablissement = fields.Char()
    prenom = fields.Char()
    ancien_corps_id = fields.Many2one('rh.corps')
    ancien_grade_id = fields.Many2one('rh.grade')
    date_ancien_grade = fields.Date()
    nature_handicap = fields.Selection([('audio', 'Audio'),
                              ('visuel', 'Visuel'),
                              ('cinetique', 'Cinetique')],
                              readonly=False,default='audio')
    taux_handicap = fields.Float()
    corps_visible = fields.Boolean(default=True)
    gender = fields.Selection(selection=[('male', 'Masculin'), ('female', 'Féminin')], readonly=False, required=True)
    place_of_birth_fr = fields.Char('Lieu de naissance', groups="hr.group_hr_user", required=True)
    groupe_id = fields.Many2one('rh.groupe', readonly=False)
    point_indiciare = fields.Integer()
    indice_minimal = fields.Integer()
    indice_base = fields.Integer()
    bonification_indiciaire = fields.Integer()
    categorie_id = fields.Many2one('rh.categorie')
    categorie_superieure_id = fields.Many2one('rh.categorie.superieure')
    echelon_id = fields.Many2one('rh.echelon')
    niveau_hierarchique_id = fields.Many2one('rh.niveau.hierarchique')
    section_id = fields.Many2one('rh.section')
    section_superieure_id = fields.Many2one('rh.section.superieure')
    grille_id = fields.Many2one('rh.grille')
    code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)
    date_avancement = fields.Date()

    @api.onchange('nature_travail_id')
    def _onchange_related_field_filier(self):
        print('teste')
        for rec in self:
            domain = []
            if rec.nature_travail_id:
                if rec.nature_travail_id.code_type_fonction == 'contractuel':
                    corps_visible = False
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                elif rec.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                    corps_visible = True
                    print('teste')
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                elif rec.nature_travail_id.code_type_fonction == 'postesuperieure':
                    corps_visible = True
                    print('teste')
                    jobs = self.env['hr.job'].search([('nature_travail_id', '=', rec.nature_travail_id.id)])
                    domain.append(('id', 'in', jobs.ids))
                else:
                    jobs = None
                    domain = None
            else:
                domain = ''

        res = {'domain': {'job_id': domain}}
        print(res)
        return res

    @api.onchange('corps_id')
    def _onchange_corps(self):
        print('teste')
        for rec in self:
            domain = []
            if rec.corps_id:
                print('teste')
                corps = self.env['rh.grade'].search([('corps_id', '=', rec.corps_id.id)])
                domain.append(('id', 'in', corps.ids))
            else:
                domain = ''

        res = {'domain': {'grade_id': domain}}
        print(res)
        return res




    
