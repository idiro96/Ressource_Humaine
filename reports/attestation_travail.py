from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AttestationTravail(models.Model):
    _inherit = 'hr.contract'

    @api.multi
    def print_report(self):
        if self.state != 'open':
            raise UserError(
                _("Ce contrat n'est pas en cours. Vous ne pouvez imprimer l'attestation que pour les contrats en cours."))

        return self.env.ref('ressource_humaine.action_attestation_travail_report').report_action(self)


class AttestationTravailReport(models.AbstractModel):
    _name = 'report.ressource_humaine.attestation_travail_report'

    @api.model
    def get_report_values(self, docids, data=None):
        contract = self.env['hr.contract'].browse(docids[0])

        report_data = {
            'contract': contract,
            'company': self.env.user.company_id,
        }

        return report_data
