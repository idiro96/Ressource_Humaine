# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError




class  HrContratInherited(models.Model):
    _inherit = 'hr.contract'

    # code_contrat = fields.Char()
    # date_debut_contrat = fields.Date()
    # date_fin_contrat = fields.Date()
    # salaire_base_contrat = fields.Float()
    # motif_contrat = fields.Char()
    # type_contrat_id = fields.Many2one('rh.type.contrat')
    type = fields.Selection([('contrat', 'Contrat'), ('decision', 'Decision'),]
                                   , required=True, default='contrat')
    point_indiciare = fields.Integer()
    categorie_id = fields.Many2one('rh.categorie')
    echelon_id = fields.Many2one('rh.echelon')
    grille_id = fields.Many2one('rh.grille')
    @api.onchange('point_indiciare')
    def onchange_sb(self):
        for contract in self:
            contract.wage = contract.point_indiciare * 45

    @api.constrains('date_start', 'date_end', 'employee_id')
    def _check_contract_overlap(self):
        for contract in self:
            overlapping_contracts = self.search([
                ('employee_id', '=', contract.employee_id.id),
                ('date_start', '<=', contract.date_end),
                ('date_end', '>=', contract.date_start),
                ('id', '!=', contract.id),
            ])
            if overlapping_contracts:
                raise ValidationError("cette employé posséde un contrat dans cette période")

        @api.depends('trial_date_end')
        def _compute_months_passed(self):
            for contract in self:
                if contract.trial_date_end:
                    enter_date = fields.Date.from_string(contract.date_start)
                    end_date = fields.Date.from_string(contract.trial_date_end)
                    months_passed = (end_date.year - enter_date.year) * 12 + end_date.month - enter_date.month
                    contract.months_passed = months_passed
                else:
                    contract.months_passed = 0

        months_passed = fields.Integer(compute='_compute_months_passed', string='Months Passed During Trial Period',
                                       store=True)

        @api.multi
        def print_report(self):
            return self.env.ref('ressource_humaine.action_hr_contract_report').report_action(self)

class HrContractReport(models.AbstractModel):
    _name = 'report.ressource_humaine.hr_contract_report'

    @api.model
    def get_report_values(self, docids, data=None):
        # Fetch the current hr.contract record based on the provided docids
        contract = self.env['hr.contract'].browse(docids[0])

        # Prepare the data you want to pass to the report template
        report_data = {
            'contract': contract,
            'company': self.env.user.company_id,
        }

        return report_data



