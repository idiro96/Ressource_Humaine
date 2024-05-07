# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RHFormationLine(models.Model):
    _name = 'rh.formation.line'
    _inherit = ['mail.thread']


    employee_id = fields.Many2one('hr.employee', tracking=True)

    formation_id = fields.Many2one('rh.formation')
    date_debut_formation_line = fields.Date(tracking=True)
    date_fin_formation_line = fields.Date(tracking=True)
    # nbr_jour_assiste = fields.Integer()
    groupe = fields.Selection(
        [('groupe1', 'Groupe 1'), ('groupe2', 'Groupe 2'), ('groupe3', 'Groupe 3'), ('groupe4', 'Groupe 4'),
         ('groupe5', 'Groupe 5')], translate=True, tracking=True)

    @api.model
    def create(self, vals):
        new_record = super(RHFormationLine, self).create(vals)

        # Post a message with the values of the tracked fields
        message_body = "تحديث قائمة المعنيين بالتكوين :<br/>"
        if 'employee_id' in vals:
            employee_name = self.env['hr.employee'].browse(vals['employee_id']).name
            message_body += f"  • تعيين الموظف: {employee_name}<br/>"
        if 'date_debut_formation_line' in vals:
            message_body += f"  • تاريخ بداية التكوين: {vals['date_debut_formation_line']}<br/>"
        if 'date_fin_formation_line' in vals:
            message_body += f"  • تاريخ إنتهاء التكوين: {vals['date_fin_formation_line']}<br/>"
        if 'groupe' in vals:
            message_body += f"  • المجموعة: {vals['groupe']}<br/>"

        if message_body:
            new_record.formation_id.message_post(body=message_body)

        return new_record

    @api.multi
    def unlink(self):
        for record in self:
            message_body = f"قد تم حذف الموظف {record.employee_id.name} من قائمة المعنيين بالتكوين"
            if message_body:
                record.formation_id.message_post(body=message_body)

        return super(RHFormationLine, self).unlink()

    def write(self, vals):
        # Store the original values of the fields before the write operation
        original_employee_id = self.employee_id
        original_date_debut = self.date_debut_formation_line
        original_date_fin = self.date_fin_formation_line
        original_groupe = self.groupe

        # Call super to perform the default behavior of write
        result = super(RHFormationLine, self).write(vals)

        # Check if any of the tracked fields have changed
        if any(field in vals for field in ['employee_id', 'date_debut_formation_line', 'date_fin_formation_line', 'groupe']):
            self._track_changes(original_employee_id, original_date_debut, original_date_fin, original_groupe)

        return result

    def _track_changes(self, original_employee_id, original_date_debut, original_date_fin, original_groupe):
        # Post a message in the chatter of the related formation record
        if self.formation_id:
            new_employee_name = self.employee_id.name if self.employee_id else False
            old_employee_name = original_employee_id.name if original_employee_id else False

            message_body = 'تحديث قائمة المعنيين بالتكوين :<br/>'
            if old_employee_name != new_employee_name:
                if old_employee_name and new_employee_name:
                    message_body += f"  • تغيير الموظف من {old_employee_name} إلى {new_employee_name}<br/>"
                elif old_employee_name:
                    message_body += f"  • حذف الموظف: {old_employee_name}<br/>"
                elif new_employee_name:
                    message_body += f"  • تعيين الموظف: {new_employee_name}<br/>"

            if self.date_debut_formation_line != original_date_debut:
                message_body += f"  • تغيير تاريخ بداية تكوين الموظف {new_employee_name} من {original_date_debut} إلى {self.date_debut_formation_line}<br/>"

            if self.date_fin_formation_line != original_date_fin:
                message_body += f"  • تغيير تاريخ إنتهاء تكوين الموظف {new_employee_name} من {original_date_fin} إلى {self.date_fin_formation_line}<br/>"

            if self.groupe != original_groupe:
                original_groupe_label = dict(self._fields['groupe'].selection).get(original_groupe, original_groupe)
                groupe_label = dict(self._fields['groupe'].selection).get(self.groupe, self.groupe)
                message_body += f"• تغيير مجموعة الموظف {new_employee_name} من {original_groupe_label} إلى {groupe_label}<br/>"

            self.formation_id.message_post(body=message_body)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        selected_employees = self.formation_id.formation_lines.mapped('employee_id')
        return {'domain': {'employee_id': [('id', 'not in', selected_employees.ids)]}}

    def formation_absence(self):
        context = {
            'default_employee_name': self.employee_id.name,
        }

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Formation absence',
            'view_mode': 'form',
            'res_model': 'absence.formation',
            'context': context,
        }
