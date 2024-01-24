# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAvancementLine(models.Model):
    _name = 'rh.avancement.line'

    date_avancement = fields.Date()
    code = fields.Char(readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('rh.avancement.line.sequence'))
    ref = fields.Char()
    date_ref = fields.Date()
    avancement_id = fields.Many2one('hr.avancement')
    employee_id = fields.Many2one('hr.employee')
    type_fonction_id = fields.Many2one('rh.type.fonction')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie')
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon')
    categorie_superieure_new_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_new_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_new_id = fields.Many2one('rh.niveau.hierarchique')

    grade_id = fields.Many2one('rh.grade')
    job_id = fields.Many2one('hr.job')
    date_old_avancement = fields.Date()

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    imprimer = fields.Boolean(Default=False)

    avancement_line_file_line = fields.Binary()




