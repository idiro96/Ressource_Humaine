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



