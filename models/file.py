# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHFile(models.Model):
    _name = 'rh.file'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'


    fichier = fields.Binary(track_visibility="onchange")
    description_fichier = fields.Char(track_visibility="onchange")
    sanction_id = fields.Many2one('rh.sanction', track_visibility="onchange")
    organisme_id = fields.Many2one('rh.organisme', track_visibility="onchange")
    fin_relation_id = fields.Many2one('rh.fin.relation', track_visibility="onchange")
    cabinet_medicale_id = fields.Many2one('rh.cabinet.medical', track_visibility="onchange")
    enfant_id = fields.Many2one('rh.enfant', track_visibility="onchange")
    conjoint_id = fields.Many2one('rh.conjoint', track_visibility="onchange")
    absence_id = fields.Many2one('rh.absence', track_visibility="onchange")
    formation_id = fields.Many2one('rh.formation', track_visibility="onchange")
    avancement_id = fields.Many2one('rh.avancement', track_visibility="onchange")
    avancement_line_id = fields.Many2one('rh.avancement.line', track_visibility="onchange")
    promotion_line_id = fields.Many2one('rh.promotion.line', track_visibility="onchange")
    promotion_id = fields.Many2one('rh.promotion_id', track_visibility="onchange")
    accident_travail_id = fields.Many2one('rh.accident_travail', track_visibility="onchange")
    type_file_id = fields.Many2one('rh.type.file', track_visibility="onchange")
    employee_id = fields.Many2one('hr.employee', track_visibility="onchange")

    @api.model
    def create(self, vals):
        new_record = super(RHFile, self).create(vals)

        # Post a message with the values of the tracked fields
        message_body = "تحديث قائمة الملفات :<br/>"
        if 'type_file_id' in vals:
            type_file_id_intitule = self.env['rh.type.file'].browse(vals['type_file_id']).intitule
            message_body += f"  • تعيين نوع الملف: {type_file_id_intitule}<br/>"
        if 'description_fichier' in vals:
            message_body += f"  • تعيين وصف الملف: {vals['description_fichier']}<br/>"

        if message_body:
            new_record.formation_id.message_post(body=message_body)
            new_record.employee_id.message_post(body=message_body)
            new_record.sanction_id.message_post(body=message_body)
            new_record.organisme_id.message_post(body=message_body)
            new_record.fin_relation_id.message_post(body=message_body)
            new_record.cabinet_medicale_id.message_post(body=message_body)
            new_record.enfant_id.message_post(body=message_body)
            new_record.conjoint_id.message_post(body=message_body)
            new_record.absence_id.message_post(body=message_body)
            new_record.avancement_id.message_post(body=message_body)
            new_record.promotion_id.message_post(body=message_body)
            new_record.accident_travail_id.message_post(body=message_body)

        return new_record

    @api.multi
    def unlink(self):
        for record in self:
            message_body = f"قد تم حذف الملف {record.description_fichier} من قائمة الملفات"
            if message_body:
                record.formation_id.message_post(body=message_body)
                record.employee_id.message_post(body=message_body)
                record.sanction_id.message_post(body=message_body)
                record.organisme_id.message_post(body=message_body)
                record.fin_relation_id.message_post(body=message_body)
                record.cabinet_medicale_id.message_post(body=message_body)
                record.enfant_id.message_post(body=message_body)
                record.conjoint_id.message_post(body=message_body)
                record.absence_id.message_post(body=message_body)
                record.avancement_id.message_post(body=message_body)
                record.promotion_id.message_post(body=message_body)
                record.accident_travail_id.message_post(body=message_body)

        return super(RHFile, self).unlink()

    def write(self, vals):
        # Store the original values of the fields before the write operation
        original_type_file_id = self.type_file_id
        original_description_fichier = self.description_fichier

        # Call super to perform the default behavior of write
        result = super(RHFile, self).write(vals)

        # Check if any of the tracked fields have changed
        if any(field in vals for field in ['type_file_id', 'description_fichier']):
            self._track_changes(original_type_file_id, original_description_fichier)

        return result

    def _track_changes(self, original_type_file_id, original_description_fichier):
        # Post a message in the chatter of the related formation record
        if (self.formation_id or self.employee_id or self.sanction_id or self.organisme_id or self.fin_relation_id or
                self.cabinet_medicale_id or self.enfant_id or self.conjoint_id or self.absence_id or self.avancement_id
                or self.promotion_id or self.accident_travail_id):
            new_type_file_id_intitule = self.type_file_id.intitule if self.type_file_id else False
            old_type_file_id_intitule = original_type_file_id.intitule if original_type_file_id else False

            message_body = 'تحديث قائمة الملفات :<br/>'
            if old_type_file_id_intitule != new_type_file_id_intitule:
                if old_type_file_id_intitule and new_type_file_id_intitule:
                    message_body += f"  • تغيير نوع الملف {old_type_file_id_intitule} إلى {new_type_file_id_intitule}<br/>"
                elif old_type_file_id_intitule:
                    message_body += f"  • حذف نوع الملف: {old_type_file_id_intitule}<br/>"
                elif new_type_file_id_intitule:
                    message_body += f"  • تعيين نوع الملف: {new_type_file_id_intitule}<br/>"

            if self.description_fichier != original_description_fichier:
                message_body += f"  • تغيير وصف الملف {new_type_file_id_intitule} من {original_description_fichier or 'بدون وصف'} إلى {self.description_fichier or 'بدون وصف'}<br/>"

            if message_body:
                self.formation_id.message_post(body=message_body)
                self.employee_id.message_post(body=message_body)
                self.sanction_id.message_post(body=message_body)
                self.organisme_id.message_post(body=message_body)
                self.fin_relation_id.message_post(body=message_body)
                self.cabinet_medicale_id.message_post(body=message_body)
                self.enfant_id.message_post(body=message_body)
                self.conjoint_id.message_post(body=message_body)
                self.absence_id.message_post(body=message_body)
                self.avancement_id.message_post(body=message_body)
                self.promotion_id.message_post(body=message_body)
                self.accident_travail_id.message_post(body=message_body)

