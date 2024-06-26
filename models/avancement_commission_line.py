# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHAvancementCommissionLine(models.Model):
    _name = 'rh.avancement.commission.line'
    # _inherit = ['mail.thread']

    employee_id = fields.Many2one('hr.employee', tracking=True)
    avancement_id = fields.Many2one('rh.avancement')
    department_id = fields.Char(tracking=True)
    job_id = fields.Char(tracking=True)
    # date_commission= fields.Date()

    # @api.model
    # def create(self, vals):
    #     new_record = super(RHAvancementCommissionLine, self).create(vals)
    #
    #     message_body = "تحديث أعضاء اللجنة :<br/>"
    #     if 'employee_id' in vals:
    #         employee_name = self.env['hr.employee'].browse(vals['employee_id']).name
    #         message_body += f"  • تعيين الموظف: {employee_name}<br/>"
    #     if 'department_id' in vals:
    #         message_body += f"  • الهيكل: {vals['department_id']}<br/>"
    #     if 'job_id' in vals:
    #         message_body += f"  • المنصب: {vals['job_id']}<br/>"
    #
    #     if message_body:
    #         new_record.avancement_id.message_post(body=message_body)
    #
    #     return new_record
    #
    # @api.multi
    # def unlink(self):
    #     for record in self:
    #         message_body = f"قد تم حذف الموظف {record.employee_id.name} من أعضاء اللجنة"
    #         if message_body:
    #             record.avancement_id.message_post(body=message_body)
    #
    #     return super(RHAvancementCommissionLine, self).unlink()
    #
    # def write(self, vals):
    #     original_employee_id = self.employee_id
    #     original_department_id = self.department_id
    #     original_job_id = self.job_id
    #
    #     result = super(RHAvancementCommissionLine, self).write(vals)
    #
    #     if any(field in vals for field in
    #            ['employee_id', 'department_id', 'job_id']):
    #         self._track_changes(original_employee_id, original_department_id, original_job_id)
    #
    #     return result
    #
    # def _track_changes(self, original_employee_id, original_department_id, original_job_id):
    #     if self.avancement_id:
    #         new_employee_name = self.employee_id.name if self.employee_id else False
    #         old_employee_name = original_employee_id.name if original_employee_id else False
    #
    #         message_body = 'تحديث أعضاء اللجنة :<br/>'
    #         if old_employee_name != new_employee_name:
    #             if old_employee_name and new_employee_name:
    #                 message_body += f"  • تغيير الموظف من {old_employee_name} إلى {new_employee_name}<br/>"
    #             elif old_employee_name:
    #                 message_body += f"  • حذف الموظف: {old_employee_name}<br/>"
    #             elif new_employee_name:
    #                 message_body += f"  • تعيين الموظف: {new_employee_name}<br/>"
    #
    #         if self.department_id != original_department_id:
    #             message_body += f"  • تغيير هيكل {new_employee_name} من {original_department_id} إلى {self.department_id}<br/>"
    #
    #         if self.job_id != original_job_id:
    #             message_body += f"  • تغيير منصب {new_employee_name} من {original_job_id} إلى {self.job_id}<br/>"
    #
    #         self.formation_id.message_post(body=message_body)
