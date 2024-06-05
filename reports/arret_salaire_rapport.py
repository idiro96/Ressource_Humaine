from datetime import datetime

from odoo import models, api, _, fields


class ArretSalaireReport(models.AbstractModel):
    _name = 'report.ressource_humaine.arret_salaire_rapport'

    @api.model
    def get_report_values(self, docids, data=None):

        decision = self.env['arret.salaire'].browse(docids[0])
        formatted_date_motif = None
        formatted_date_avancement = None
        formatted_date_arret_salaire = None
        formatted_date_titularisation = None
        formatted_date_decision_titularisation = None
        if decision.date_motif:
            rapport_date_motif = decision.date_motif
            formatted_date_motif = datetime.strptime(rapport_date_motif, "%Y-%m-%d").strftime("%Y/%m/%d")
        if decision.employee_id.date_avancement:
            rapport_date_avancement = decision.employee_id.date_avancement
            formatted_date_avancement = datetime.strptime(rapport_date_avancement, "%Y-%m-%d").strftime("%Y/%m/%d")
        if decision.date_arret_salaire:
            rapport_date_arret_salaire = decision.date_arret_salaire
            formatted_date_arret_salaire = datetime.strptime(rapport_date_arret_salaire, "%Y-%m-%d").strftime(
                "%Y/%m/%d")
        if decision.date_titularisation:
            rapport_date_titularisation = decision.date_titularisation
            formatted_date_titularisation = datetime.strptime(rapport_date_titularisation,
                                                              "%Y-%m-%d").strftime("%Y/%m/%d")
        if decision.date_decision_titularisation:
            rapport_date_decision_titularisation = decision.date_decision_titularisation
            formatted_date_decision_titularisation = datetime.strptime(rapport_date_decision_titularisation,
                                                                       "%Y-%m-%d").strftime("%Y/%m/%d")

        # nom_employee = self.env['rh.fin.relation'].browse(docids)
        # print(nom_employee)
        # nom_employee2 = self.env['rh.fin.relation'].browse(docids[0]).employee_id
        # employee = self.env['hr.employee'].browse(docids)
        # promotion = self.env['rh.promotion.line'].search([('employee_id', '=', nom_employee2.id)])
        # date_grade = nom_employee.employee_id.date_grade
        # formatted_date = datetime.strptime(date_grade, "%Y-%m-%d").strftime("%d-%m-%Y")
        # # info_promotion = self.env['rh.promotion'].search([('id', '=', promotion.promotion_id)])
        # # promo = self.env['rh.promotion'].search([('promotion_lines.employee_id', '=', nom_employee2.id)])
        # promo = self.env['rh.promotion'].search([('promotion_lines.employee_id', '=', nom_employee2.id)])

        report_data = {
            'decision': decision,
            'date_motif': formatted_date_motif,
            'date_avancement': formatted_date_avancement,
            'date_arret_salaire': formatted_date_arret_salaire,
            'date_titularisation': formatted_date_titularisation,
            'date_decision_titularisation': formatted_date_decision_titularisation,
            # 'nom_employee': nom_employee,
            # 'employee': employee,
            # 'promotion': promotion,
            # 'date_grade': formatted_date,
            # 'promo': promo,
            # 'company': self.env.user.company_id,
        }
        return report_data
