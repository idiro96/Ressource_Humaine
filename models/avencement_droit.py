# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


class RHAvencementDroit(models.Model):
    _name = 'rh.avencement.droit'

    employee_id = fields.Many2one('hr.employee')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie')
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon')

    sauvegarde = fields.Boolean(Default=False)
    test = fields.Char()
    date_avancement = fields.Date()
    # @api.multi
    # def write(self, vals):
    #     res = super(RHAvencementDroit, self).write(vals)
    #     for rec in self:
    #         if rec.sauvegarde != False
    #     res1 = self.env['account.asset.asset'].search([('id', '=', self.id)])
