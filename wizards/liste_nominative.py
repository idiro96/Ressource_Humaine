from odoo import models, fields, api, _


class ListeNominative(models.TransientModel):
    _name = 'liste.nominative'

    @api.multi
    def print_report(self):

        return self.env.ref('ressource_humaine.action_liste_nominative').report_action(self)