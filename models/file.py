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
    fin_relation_id = fields.Many2one('rh.fin_relation', track_visibility="onchange")
    cabinet_medicale_id = fields.Many2one('rh.fin_relation', track_visibility="onchange")
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
