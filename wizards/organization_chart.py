from odoo import models, fields, api, _


class OrganizationChart(models.TransientModel):
    _name = 'organization.chart'

    @api.multi
    def print_report(self):
        return self.env.ref('ressource_humaine.action_organization_chart').report_action(self)


class OrganizationChartReport(models.AbstractModel):
    _name = 'report.ressource_humaine.organization_chart_report'

    @api.model
    def get_report_values(self, docids, data=None):
        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الموارد البشرية'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الموارد البشرية'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        ressource_humaine = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الميزانية'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الميزانية'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        budget_comptabilite = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الإعلام'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الإعلام'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        informatique = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الوسائل العامة'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'الوسائل العامة'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        mgx = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'النظام الداخلي'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'النظام الداخلي'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        internat = high_position_employees + other_employees



        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', '%مديرية الدرسات%'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', '%مديرية الدرسات%'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        etude = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'التربصات'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'التربصات'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        stage = high_position_employees + other_employees


        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'التكوين'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'التكوين'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        formation = high_position_employees + other_employees



        high_position_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'البحث'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '=', 'منصب عالي')
        ], order='indice_base desc')

        other_employees = self.env['hr.employee'].search([
            ('department_id.complete_name', 'ilike', 'البحث'),
            ('fin_relation', '=', False),
            ('nature_travail_id', '!=', 'منصب عالي')
        ], order='indice_minimal desc')

        recherche = high_position_employees + other_employees


        report_data = {
            'company': self.env.user.company_id,
            'ressource_humaine': ressource_humaine,
            'budget_comptabilite': budget_comptabilite,
            'informatique': informatique,
            'mgx': mgx,
            'internat': internat,
            'etude': etude,
            'stage': stage,
            'formation': formation,
            'recherche': recherche,
        }

        return report_data
