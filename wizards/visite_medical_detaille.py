# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHVisiteMedicalDetaille(models.TransientModel):
    _name = 'visite.medical.detaille'


    employee_id_lines = fields.One2many('hr.employee', 'visite_medical_detaille_id', string="Visite Medical Lines", default=lambda self: self._default_employees())

    date_visite_medicale = fields.Date()


    def detaille_viste_medical(self):
        print(self.employee_id_lines)
        record = self.env['rh.visite.medicale'].browse(self._context['active_id'])
        for line in self.employee_id_lines:
            print('IDIR')
            print(line)
            if line.selection_employe_visite_medicale == True:
                print('IDIR2')
                print(line)
                visite_medical = self.env['rh.visite.medical.line'].create({
                'employee_id': line.id,
                'visite_medical_id':record.id,
                'date_visite_medicale': self.date_visite_medicale,
                })
                print('fffffffffffffffffffffffffff')
                print(line.id)
                print(line.id)

        # record = self.env['rh.visite.medicale'].browse(self._context['active_id'])
        # records = self.env['visite.medical.detaille'].browse(self.employee_id_lines)
        #
        # for rec in records:
        #     visite_medical = self.env['rh.visite.medical.line'].create({
        #
        #         'employee_id': rec.id,
        #         'date_visite_medicale': self.date_visite_medicale,
        # })

    @api.model
    def _default_employees(self):
        return self.env['hr.employee'].search([])

    # @api.model
    # def detaille_viste_medical(self):
    #     for rec1 in self.employee_id_lines.:
    #         print(rec1)
    #         if rec1.selection_employe_visite_medicale == True:
    #             visite_medical_Detail = self.env['rh.visite.medical.line'].create({
    #                 'employee_id': rec1.id,
    #                 'visite_medical_id': self.visite_medical_id.id,
    #                 'date_visite_medicale': self.date_visite_medicale,
    #             })





