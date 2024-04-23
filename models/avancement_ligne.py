# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _


class RHAvancementLine(models.Model):
    _name = 'rh.avancement.line'
    _inherit = ['mail.thread']

    date_avancement = fields.Date(tracking=True)
    code = fields.Char(readonly=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('rh.avancement.line.sequence'),
                       tracking=True)
    ref = fields.Char(tracking=True)
    date_ref = fields.Date(tracking=True)
    avancement_id = fields.Many2one('rh.avancement')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    date_signature = fields.Date(related='avancement_id.date_signature', tracking=True)
    type_fonction_id = fields.Many2one('rh.type.fonction')
    grille_old_id = fields.Many2one('rh.grille', tracking=True)
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie', tracking=True)
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon', tracking=True)
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    grille_new_id = fields.Many2one('rh.grille', tracking=True)
    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie', tracking=True)
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon', tracking=True)
    categorie_superieure_new_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_new_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_new_id = fields.Many2one('rh.niveau.hierarchique')

    grade_id = fields.Many2one('rh.grade', tracking=True)
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date(tracking=True)
    date_new_avancement = fields.Date(tracking=True)
    duree = fields.Integer(tracking=True)
    duree_lettre = fields.Selection(
        selection=[('inferieure', 'Inferieure'), ('moyen', 'Moyen'), ('superieure', 'Supérieure')])

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()

    avancement_line_file_line = fields.Binary(track_visibility='onchange')
    ancien_index = fields.Integer(tracking=True)

    @api.depends('date_new_avancement', 'avancement_id.date_avancement')
    def _compute_time(self):
        for rec in self:
            if rec.date_new_avancement and rec.avancement_id.date_avancement:
                date_new_avancement = fields.Datetime.from_string(rec.date_new_avancement)
                date_avancement = fields.Datetime.from_string(rec.avancement_id.date_avancement)
                delta = relativedelta(date_avancement, date_new_avancement)

                years = delta.years
                months = delta.months
                days = delta.days

                rec.time_years = years
                rec.time_months = months
                rec.time_days = days

    time_years = fields.Integer(compute="_compute_time", store=True)
    time_months = fields.Integer(compute="_compute_time", store=True)
    time_days = fields.Integer(compute="_compute_time", store=True)

    # @api.model
    # def create(self, vals):
    #     new_record = super(RHAvancementLine, self).create(vals)
    #
    #     # Post a message with the values of the tracked fields
    #     message_body = "الترقيات في الدرجة :<br/>"
    #     if 'employee_id' in vals:
    #         employee_name = self.env['hr.employee'].browse(vals['employee_id']).name
    #         message_body += f"  • الموظف: {employee_name}<br/>"
    #     if 'grade_id' in vals:
    #         intitule_grade = self.env['rh.grade'].browse(vals['grade_id']).intitule_grade
    #         message_body += f"  • الرتبة: {intitule_grade}<br/>"
    #     if 'ref' in vals:
    #         message_body += f"  • رقم المقرر: {vals['ref']}<br/>"
    #     if 'date_ref' in vals:
    #         message_body += f"  • تاريخ مقرر آخر ترقية: {vals['date_ref']}<br/>"
    #     if 'date_old_avancement' in vals:
    #         message_body += f"  • تاريخ آخر ترقية في الدرجة: {vals['date_old_avancement']}<br/>"
    #     if 'grille_old_id' in vals:
    #         grille_old_id_desc = self.env['rh.grille'].browse(vals['grille_old_id']).description_grille
    #         message_body += f"  • الشبكة القديمة: {grille_old_id_desc}<br/>"
    #     if 'categorie_old_id' in vals:
    #         categorie_old_id_intitule = self.env['rh.categorie'].browse(vals['categorie_old_id']).intitule
    #         message_body += f"  • الصنف السابق: {categorie_old_id_intitule}<br/>"
    #     if 'echelon_old_id' in vals:
    #         echelon_old_id_intitule = self.env['rh.echelon'].browse(vals['echelon_old_id']).intitule
    #         message_body += f"  • الدرجة السابقة: {echelon_old_id_intitule}<br/>"
    #     if 'date_new_avancement' in vals:
    #         message_body += f"  • تاريخ سريان الترقية القادمة: {vals['date_new_avancement']}<br/>"
    #     if 'code' in vals:
    #         message_body += f"  • الكود: {vals['code']}<br/>"
    #     if 'date_signature' in vals:
    #         message_body += f"  • تاريخ الإمضاء: {vals['date_signature']}<br/>"
    #     if 'duree' in vals:
    #         message_body += f"  • المدة: {vals['duree']}<br/>"
    #     if 'grille_new_id' in vals:
    #         grille_new_id_desc = self.env['rh.grille'].browse(vals['grille_new_id']).description_grille
    #         message_body += f"  • الشبكة الجديدة: {grille_new_id_desc}<br/>"
    #     if 'categorie_new_id' in vals:
    #         categorie_new_id_intitule = self.env['rh.categorie'].browse(vals['categorie_new_id']).intitule
    #         message_body += f"  • الصنف الحالي: {categorie_new_id_intitule}<br/>"
    #     if 'echelon_new_id' in vals:
    #         echelon_new_id_intitule = self.env['rh.echelon'].browse(vals['echelon_new_id']).intitule
    #         message_body += f"  • الدرجة الحالية: {echelon_new_id_intitule}<br/>"
    #     if 'date_avancement' in vals:
    #         message_body += f"  • تاريخ الإستفادة: {vals['date_avancement']}<br/>"
    #     if 'ancien_index' in vals:
    #         message_body += f"  • رقم إستدلالي للطلبة: {vals['ancien_index']}<br/>"
    #
    #     if message_body:
    #         new_record.employee_id.message_post(body=message_body)
    #         new_record.avancement_id.message_post(body=message_body)
    #
    #     return new_record

    @api.multi
    def unlink(self):
        for record in self:
            message_body = f"قد تم حذف الموظف {record.employee_id.name} من قائمة الموظفين"
            if message_body:
                record.avancement_id.message_post(body=message_body)

        return super(RHAvancementLine, self).unlink()

    def write(self, vals):
        # Store the original values of the fields before the write operation
        original_ref = self.ref
        original_date_ref = self.date_ref
        original_code = self.code
        original_date_signature = self.date_signature
        original_ancien_index = self.ancien_index

        # Call super to perform the default behavior of write
        result = super(RHAvancementLine, self).write(vals)

        # Check if any of the tracked fields have changed
        if any(field in vals for field in
               ['ref', 'date_ref', 'code', 'date_signature', 'ancien_index']):
            self._track_changes(original_ref, original_date_ref, original_code, original_date_signature, original_ancien_index)

        return result

    def _track_changes(self, original_ref, original_date_ref, original_code, original_date_signature, original_ancien_index):
        # Post a message in the chatter of the related formation record
        if self.employee_id or self.avancement_id:
            employee_name = self.employee_id.name if self.employee_id else False

            message_body = 'تحديث الترقيات في الدرجة :<br/>'
            if self.ref != original_ref:
                message_body += f"  • تغيير رقم مقرر {employee_name} من {original_ref} إلى {self.ref}<br/>"

            if self.date_ref != original_date_ref:
                message_body += f"  • تغيير تاريخ مقرر آخر ترقية {employee_name} من {original_date_ref} إلى {self.date_ref}<br/>"

            if self.code != original_code:
                message_body += f"  • تغيير كود {employee_name} من {original_code} إلى {self.code}<br/>"

            if self.date_signature != original_date_signature:
                message_body += f"  • تغيير تاريخ إمضاء {employee_name} من {original_date_signature} إلى {self.date_signature}<br/>"

            if self.ancien_index != original_ancien_index:
                message_body += f"  • تغيير الرقم الإستدلالي لطلبة {employee_name} من {original_ancien_index} إلى {self.ancien_index}<br/>"

            self.employee_id.message_post(body=message_body)
            self.avancement_id.message_post(body=message_body)
