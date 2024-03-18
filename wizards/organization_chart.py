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
        ressource_humaine = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الموارد البشرية')])
        budget_comptabilite = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الميزانية')])
        informatique = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الإعلام')])
        mgx = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'الوسائل العامة')])
        internat = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'النظام الداخلي')])
        etude = self.env['hr.employee'].search(['|', ('department_id.complete_name', 'ilike', '%مديرية الدراسات%'),
                                                ('department_id.complete_name', 'ilike', '%مديرية الدرسات%')])
        stage = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التربصات')])
        formation = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'التكوين')])
        recherche = self.env['hr.employee'].search([('department_id.complete_name', 'ilike', 'البحث')])

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
