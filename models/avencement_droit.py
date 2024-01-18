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
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie')
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon')
    echelon_new_id = fields.Many2one('rh.echelon')

    test = fields.Char()

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_droit_avancement_report').report_action(self)


class DroitAvancementReport(models.AbstractModel):
    _name = 'report.ressource_humaine.droit_avancement_report'

    @api.model
    def get_report_values(self, docids, data=None):
        avancement = self.env['rh.avencement.droit'].browse(docids[0])

        report_data = {
            'avancement': avancement,
            'company': self.env.user.company_id,
        }

        return report_data
