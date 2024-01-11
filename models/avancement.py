# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAvancement(models.Model):
    _name = 'rh.avancement'

    date_avancement = fields.Date()
    code = fields.Char()
    avancement_lines = fields.One2many('rh.avancement.line', inverse_name='avancement_id')
    avancement_lines_wizard = fields.One2many('rh.avancement.line.wizard', inverse_name='avancement_id')

    # promotion_file_lines = fields.One2many('rh.file', 'promotion_id')



    @api.onchange('date_avancement')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        print('teste')
        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_wizard1 = self.env['rh.avancement.line.wizard'].search([])
        for record in avancement_ligne_wizard1:
            record.unlink()
        for rec in employee:
            print(rec.id)

            avancement_line = self.env['rh.avancement.line'].search([('employee_id', '=', rec.id),('date_avancement', '<=',self.date_avancement)],
                                                            order='date_avancement desc', limit=1)
            if avancement_line:
                self.env['rh.avancement.line.wizard'].create({
                'employee_id': avancement_line.employee_id.id,
                'avancement_id': avancement_line.avancement_id.id,
                'categorie_new_id': avancement_line.categorie_new_id.id,
                'section_new_id': avancement_line.section_new_id.id,
                'echelon_new_id': avancement_line.echelon_new_id.id

            })
        self.avancement_lines_wizard = self.env['rh.avancement.line.wizard'].search([])
        return {
                'type': 'ir.actions.act_window',
                'target': 'new',
                'name': 'Avancement',
                'view_mode': 'form',
                'res_model': 'rh.avancement',
            }


