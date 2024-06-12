# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RHPromotionLine(models.Model):
    _name = 'rh.promotion.line'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _mail_post_access = 'read'

    date_examin_professionnel = fields.Date()
    date_promotion = fields.Date()
    promotion_id = fields.Many2one('rh.promotion')
    employee_id = fields.Many2one('hr.employee')
    birthday = fields.Date(related='employee_id.birthday')
    marital = fields.Selection(related='employee_id.marital')
    job_id = fields.Many2one('hr.job')
    grade_old_id = fields.Many2one('rh.grade')
    grade_id = fields.Many2one('rh.grade')
    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    date_grade = fields.Date()
    type_fonction_id = fields.Many2one('rh.type.fonction')
    promotion_line_file_line = fields.Binary()
    duree = fields.Integer()
    imprimer = fields.Boolean(Default=False)
    code_line = fields.Char(tracking=True)
    date_creation = fields.Char(compute="_compute_date", store=True)
    ref_promotion = fields.Char()
    date_ref_promotion = fields.Date()
    date_signature = fields.Date(related='promotion_id.date_signature')
    ancien_index = fields.Integer(tracking=True)
    categorie_id = fields.Many2one('rh.categorie')
    section_id = fields.Many2one('rh.section')
    echelon_id = fields.Many2one('rh.echelon')
    employee_index = fields.Integer()
    date_avancement = fields.Date()
    ref = fields.Char()
    date_ref = fields.Date()

    @api.depends('code_line')
    def _compute_date(self):
        for record in self:
            if record.create_date:
                # Convertit le champ en un objet datetime
                datetime_object = record.create_date.split(' ')
                # Récupère uniquement la date
                date_creation = datetime_object[0]
                record.date_creation = date_creation

    # @api.multi
    # def unlink(self):
    #     for record in self:
    #         message_body = f"قد تم حذف الموظف {record.employee_id.name} من قائمة الموظفين"
    #         if message_body:
    #             record.promotion_id.message_post(body=message_body)
    #
    #     return super(RHPromotionLine, self).unlink()
    #
    # def write(self, vals):
    #     original_code_line = self.code_line
    #     original_ancien_index = self.ancien_index
    #
    #     result = super(RHPromotionLine, self).write(vals)
    #
    #     if any(field in vals for field in
    #            ['code_line', 'ancien_index']):
    #         self._track_changes(original_code_line, original_ancien_index)
    #
    #     return result
    #
    # def _track_changes(self, original_code_line, original_ancien_index):
    #     if self.promotion_id:
    #         message_body = 'تحديث قائمة الموظفين:<br/>'
    #         if self.code_line != original_code_line:
    #             message_body += f"  • تغيير رقم مقرر {self.employee_id.name} من {original_code_line} إلى {self.code_line}<br/>"
    #
    #         if self.ancien_index != original_ancien_index:
    #             message_body += f"  • تغيير الرقم الإستدلالي لطلبة {self.employee_id.name} من {original_ancien_index} إلى {self.ancien_index}<br/>"
    #
    #         self.promotion_id.message_post(body=message_body)

