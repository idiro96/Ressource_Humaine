# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


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
    # @api.multi
    # def write(self, vals):
    #     res = super(RHAvencementDroit, self).write(vals)
    #     for rec in self:
    #         if rec.sauvegarde != False
    #     res1 = self.env['account.asset.asset'].search([('id', '=', self.id)])

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
