# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAvancementLine(models.TransientModel):
    _name = 'rh.avancement.line.wizard'

    date_avancement = fields.Date()
    avancement_id = fields.Many2one('hr.avancement')
    employee_id = fields.Many2one('hr.employee')
    groupe_old_id = fields.Many2one('rh.groupe')
    categorie_old_id = fields.Many2one('rh.categorie')
    section_old_id = fields.Many2one('rh.section')
    echelon_old_id = fields.Many2one('rh.echelon')
    echelon_old_id = fields.Many2one('rh.echelon')
    categorie_superieure_old_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_old_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_old_id = fields.Many2one('rh.niveau.hierarchique')

    groupe_new_id = fields.Many2one('rh.groupe')
    categorie_new_id = fields.Many2one('rh.categorie')
    section_new_id = fields.Many2one('rh.section')
    echelon_new_id = fields.Many2one('rh.echelon')
    echelon_new_id = fields.Many2one('rh.echelon')
    categorie_superieure_new_id = fields.Many2one('rh.categorie.superieure')
    section_superieure_new_id = fields.Many2one('rh.section.superieure')
    niveau_hierarchique_new_id = fields.Many2one('rh.niveau.hierarchique')


    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()




