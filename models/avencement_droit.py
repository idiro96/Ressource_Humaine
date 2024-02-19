# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

from odoo.exceptions import UserError


class RHAvencementDroit(models.Model):
    _name = 'rh.avencement.droit'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    grille_old_id = fields.Many2one('rh.grille')
    grille_new_id = fields.Many2one('rh.grille')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe',)
    categorie_new_id = fields.Many2one('rh.categorie', domain="[('groupe_id', '=', groupe_new_id)]")
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon', domain="[('categorie_id', '=', categorie_new_id)]")

    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date()
    date_new_avancement = fields.Date()

    sauvegarde = fields.Boolean(Default=False)
    retenue = fields.Boolean(Default=False)
    test = fields.Char()
    date_avancement = fields.Date()
    duree = fields.Integer()
    duree_lettre = fields.Selection(selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')])
    time_years = fields.Integer(compute="_compute_time", store=True)
    time_months = fields.Integer(compute="_compute_time", store=True)
    time_days = fields.Integer(compute="_compute_time", store=True)
    time_difference = fields.Char(compute="_compute_time")
    def _compute_time(self):
        for rec in self:
            if rec.date_old_avancement and rec.date_new_avancement:
                date_old_avancement = fields.Datetime.from_string(rec.date_old_avancement)
                date_new_avancement = fields.Datetime.from_string(rec.date_new_avancement)
                delta = relativedelta(date_new_avancement, date_old_avancement)

                years = delta.years
                months = delta.months
                days = delta.days

                rec.time_years = years
                rec.time_months = months
                rec.time_days = days

                rec.time_difference = str(years) + ' annee et ' + str(months) + ' mois et ' + str(days) + 'jours'
                print(rec.time_difference)
                print('rec.time_difference')


    # @api.multi
    # def write(self, vals):
    #     res = super(RHAvencementDroit, self).write(vals)
    #     for rec in self:
    #         if rec.sauvegarde != False
    #     res1 = self.env['account.asset.asset'].search([('id', '=', self.id)])

    @api.multi
    def write(self, vals):
        result1 = super(RHAvencementDroit, self).write(vals)
        # record1 = self.env['rh.avancement.droit'].browse(self._context['active_ids'])
        for rec in self:
            print('ranah22')
            if rec.retenue:
                print('ranah223')
                if not rec.sauvegarde:
                    print('ranah224')
                    raise UserError("confirmer d'abord le droit à l'avancement d'echelon")
            record2 = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_avancement', '=', rec.date_avancement)])
            if record2:
                raise UserError("Impossible de modifier un avancement d'echelon déja validé")

        return result1

    @api.onchange('duree')
    def _onchange_duree(self):
        for rec in self:
            rec.date_new_avancement = relativedelta(months=rec.duree) + fields.Date.from_string(rec.date_old_avancement)
            if rec.duree == 30:
                rec.duree_lettre = 'inferieure'
            elif rec.duree == 36:
                rec.duree_lettre = 'moyen'
            else:
                rec.duree_lettre = 'superieure'

    @api.onchange('groupe_new_id')
    def _onchange_groupe_new_id(self):
        if self.groupe_new_id:
            self.categorie_new_id = False
            self.echelon_new_id = False
            return {'domain': {'categorie_new_id': [('groupe_id', '=', self.groupe_new_id.id)]}}
        else:
            return {'domain': {'categorie_new_id': []}}

    @api.onchange('grille_id')
    def _onchange_grille_id(self):
        if self.grille_id:
            self.groupe_new_id = False
            self.categorie_new_id = False
            self.echelon_new_id = False
            return {'domain': {'groupe_new_id': [('grille_id', '=', self.grille_id.id)]}}
        else:
            return {'domain': {'groupe_new_id': []}}

    @api.onchange('categorie_new_id')
    def _onchange_categorie_new_id(self):
        if self.categorie_new_id:
            self.echelon_new_id = False
            return {'domain': {'echelon_new_id': [('categorie_id', '=', self.categorie_new_id.id)]}}
        else:
            return {'domain': {'echelon_new_id': []}}
    @api.multi
    def print_promotion(self):
        return self.env.ref('ressource_humaine.action_hr_tableau_promotion').with_context(landscape=True).report_action(self)
