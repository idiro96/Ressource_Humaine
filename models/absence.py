# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAbsence(models.Model):
    _name = 'rh.absence'

    num_reference_absence = fields.Integer()
    date_debut_absence = fields.Date()
    date_fin_absence = fields.Date()
    nbr_jours_absence = fields.Integer()
    nbre_heure_absence = fields.Integer()
    state = fields.Selection([('draft', 'Brouillon'), ('attente', 'attente'),('valide', 'Validé'),('refuse', 'Refusé')], default='draft')
    employee_id = fields.Many2one('hr.employee')
    type_absence_id = fields.Many2one('rh.type.absence')
    def envoyer(self):
        self.state = 'attente'

    def valider(self):
        self.state = 'valide'
    def refuser(self):
        self.state = 'refuse'



