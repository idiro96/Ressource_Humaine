from odoo import models, api, _, fields


class RapportRetraite(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.retraite_report').report_action(self)



class RapportRetraiteReport(models.AbstractModel):
    _name = 'report.ressource_humaine.rapport_retraite'

    @api.model
    def get_report_values(self, docids, data=None):
        nom_employee = self.env['rh.fin.relation'].browse(docids)
        nom_employee2= self.env['rh.fin.relation'].browse(docids[0]).employee_id
        employee= self.env['hr.employee'].browse(docids)
        promotion = self.env['rh.promotion.line'].search([('employee_id', '=', nom_employee2.id)])
        promo = self.env['rh.promotion'].search([('promotion_lines.employee_id', '=', nom_employee2.id)])

        report_data = {
            'nom_employee': nom_employee,
            'employee': employee,
            'promotion': promotion,
            'promo': promo,
            'company': self.env.user.company_id,
        }
        return report_data
