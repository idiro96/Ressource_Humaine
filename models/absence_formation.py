# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHAbsenceFormation(models.Model):
    _name = 'rh.absence.formation'
    _rec_name = 'employee_id'
    # _inherit = ['mail.thread']

    formation_line_id = fields.Many2one('rh.formation.line')
    formation_id = fields.Many2one('rh.formation')
    employee_id = fields.Many2one('hr.employee', tracking=True)
    date_absence = fields.Date(tracking=True)

    # @api.model
    # def create(self, vals):
    #     new_record = super(RHAbsenceFormation, self).create(vals)
    #
    #     # Post a message with the values of the tracked fields
    #     message_body = "تحديث قائمة الغيابات :<br/>"
    #     if 'employee_id' in vals:
    #         employee_name = self.env['hr.employee'].browse(vals['employee_id']).name
    #         message_body += f"  • تعيين الموظف: {employee_name}<br/>"
    #     if 'date_absence' in vals:
    #         message_body += f"  • تاريخ الغياب: {vals['date_absence']}<br/>"
    #
    #     if message_body:
    #         new_record.formation_id.message_post(body=message_body)
    #
    #     return new_record
    #
    # @api.multi
    # def unlink(self):
    #     for record in self:
    #         message_body = f"قد تم حذف الموظف {record.employee_id.name} من قائمة الغيابات"
    #         if message_body:
    #             record.formation_id.message_post(body=message_body)
    #
    #     return super(RHAbsenceFormation, self).unlink()
    #
    # def write(self, vals):
    #     # Store the original values of the fields before the write operation
    #     original_employee_id = self.employee_id
    #     original_date_absence = self.date_absence
    #
    #     # Call super to perform the default behavior of write
    #     result = super(RHAbsenceFormation, self).write(vals)
    #
    #     # Check if any of the tracked fields have changed
    #     if any(field in vals for field in
    #            ['employee_id', 'date_absence']):
    #         self._track_changes(original_employee_id, original_date_absence)
    #
    #     return result
    #
    # def _track_changes(self, original_employee_id, original_date_absence):
    #     # Post a message in the chatter of the related formation record
    #     if self.formation_id:
    #         new_employee_name = self.employee_id.name if self.employee_id else False
    #         old_employee_name = original_employee_id.name if original_employee_id else False
    #
    #         message_body = 'تحديث قائمة الغيابات :<br/>'
    #         if old_employee_name != new_employee_name:
    #             if old_employee_name and new_employee_name:
    #                 message_body += f"  • تغيير الموظف من {old_employee_name} إلى {new_employee_name}<br/>"
    #             elif old_employee_name:
    #                 message_body += f"  • حذف الموظف: {old_employee_name}<br/>"
    #             elif new_employee_name:
    #                 message_body += f"  • تعيين الموظف: {new_employee_name}<br/>"
    #
    #         if self.date_absence != original_date_absence:
    #             message_body += f"  • تغيير تاريخ غياب {new_employee_name} من {original_date_absence} إلى {self.date_absence}<br/>"
    #
    #         self.formation_id.message_post(body=message_body)
