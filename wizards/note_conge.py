from odoo import models, fields, api, _


class NoteCongeWizard(models.TransientModel):
    _name = 'note.conge'

    code = fields.Char()

    def print_report(self):
        return self.env.ref('ressource_humaine.new_report_note_conge').report_action(self)


class NoteCongeWizardReport(models.AbstractModel):
    _name = 'report.ressource_humaine.note_conge'

    @api.model
    def get_report_values(self, docids, data=None):
        data = self.env['note.conge'].browse(docids[0])

        report_data = {
            'code': data.code,
        }

        return report_data
