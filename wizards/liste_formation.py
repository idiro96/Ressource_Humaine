# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ListeFormation(models.TransientModel):
    _name = 'liste.formation.wizard'

    date_debut = fields.Date(translate=True, required=True)
    date_fin = fields.Date(translate=True, required=True)

    @api.one
    @api.constrains('date_debut', 'date_fin')
    def check_dates(self):
        if self.date_debut and self.date_fin and self.date_debut > self.date_fin:
            raise UserError(_("La date début doit être antérieure à la date fin."))

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_liste_formation_report').report_action(self)


class ListeFormationReport(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_formation_report'

    @api.model
    def get_report_values(self, docids, data=None):
        formation_wizard = self.env['liste.formation.wizard'].browse(docids[0])
        formations = self.env['rh.formation'].search([('date_debut_formation', '>=', formation_wizard.date_debut),
                                                      ('date_fin_formation', '<=', formation_wizard.date_fin)])

        formation_lines = []
        for formation in formations:
            formation_lines.extend(formation.formation_lines)

        print(formations)
        print(formation_lines)

        report_date_debut = formation_wizard.date_debut
        date_debut = datetime.strptime(report_date_debut, "%Y-%m-%d").strftime("%Y/%m/%d")
        report_date_fin = formation_wizard.date_fin
        date_fin = datetime.strptime(report_date_fin, "%Y-%m-%d").strftime("%Y/%m/%d")
        formatted_formations = []
        for formation in formations:
            date_debut_formation = datetime.strptime(formation.date_debut_formation, "%Y-%m-%d").strftime("%Y/%m/%d")
            date_fin_formation = datetime.strptime(formation.date_fin_formation, "%Y-%m-%d").strftime("%Y/%m/%d")
            formatted_formations.append({
                'id': formation.id,
                'organisme_id': formation.organisme_id.rs_organisme,
                'date_debut_formation': date_debut_formation,
                'date_fin_formation': date_fin_formation,
                'intitule_formation': formation.intitule_formation,
                'formation_lines': formation.formation_lines,
            })

        report_data = {
            'formation_wizard': formation_wizard,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'formation_lines': formation_lines,
            'formation_lines_sizes': {formation.id: len(formation.formation_lines) for formation in formations},
            'formations': formatted_formations,
            'company': self.env.user.company_id,
        }

        return report_data
