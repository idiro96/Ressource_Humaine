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

    def export_report(self):
        return self.env.ref('ressource_humaine.action_liste_formation_xlsx').report_action(self)


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


class ListeFormationXLS(models.AbstractModel):
    _name = 'report.ressource_humaine.liste_formation_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        formation_wizard = self._get_objs_for_report(objs.ids, data)
        formation_lines = self.env['rh.formation.line'].search(
            [('formation_id.date_debut_formation', '>=', formation_wizard.date_debut),
             ('formation_id.date_fin_formation', '<=', formation_wizard.date_fin)])
        report_date_debut = formation_wizard.date_debut
        date_debut = datetime.strptime(report_date_debut, "%Y-%m-%d").strftime("%Y/%m/%d")
        report_date_fin = formation_wizard.date_fin
        date_fin = datetime.strptime(report_date_fin, "%Y-%m-%d").strftime("%Y/%m/%d")

        format1 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format1.set_text_wrap()
        format1.set_align('center')
        format1.set_valign('vcenter')
        format2 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D3D3D3', 'bold': True})
        format2.set_text_wrap()
        format2.set_align('center')
        format2.set_valign('vcenter')
        format3 = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#FFFFFF'})
        date_format = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                                           'bg_color': '#FFFFFF', 'num_format': 'J MMMM AAAA'})
        date_format2 = workbook.add_format({'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
                                            'bg_color': '#FFFFFF', 'num_format': 'AAAA - MM - JJ'})
        title_format = workbook.add_format(
            {'bold': True, 'font_size': 32, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'bg_color': '#FFFFFF'})
        sheet = workbook.add_worksheet('قائمة الموظفين المستفيدين من التكوين')
        sheet.right_to_left()

        sheet.set_row(6, 40)
        for row_num in range(7, 1000):
            sheet.set_row(row_num, 35)

        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 1, 40)
        sheet.set_column(2, 2, 25)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 30)

        sheet.write(6, 0, 'الإسم و اللقب', format1)
        sheet.write(6, 1, 'الرتبة/الوظيفة', format1)
        sheet.write(6, 2, 'موضوع الدورة التكوينية', format1)
        sheet.write(6, 3, 'المدة و التاريخ', format1)
        sheet.write(6, 4, 'ملاحــــــظة', format1)

        sheet.merge_range('A2:F4', f"{date_fin} إلى {date_debut}قائمة الموظفين المستفيدين من التكوين من ",
                          title_format)

        row = 7
        for index, line in enumerate(formation_lines, start=1):
            sheet.write(row, 0, line.employee_id.name, format3)
            sheet.write(row, 1, line.employee_id.grade_id.intitule_grade, format3)
            sheet.write(row, 2, line.formation_id.intitule_formation, format3)
            sheet.write(row, 3, f"{line.formation_id.date_fin_formation} / {line.formation_id.date_debut_formation}", format3)
            sheet.write(row, 4, line.formation_id.organisme_id.rs_organisme or '/', format3)
            row += 1
