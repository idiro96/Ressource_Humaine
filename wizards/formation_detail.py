# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RHFormationDetail(models.TransientModel):
    _name = 'formation.detail'


    # employee_id_lines = fields.One2many('hr.employee','formation_detail_id', string="Formation Lines", default=lambda self: self._default_employees())

    formation_id = fields.Many2one('rh.formation')
    #date_visite_medicale = fields.Date()

    # def detaille_viste_medical(self):
    #     record = self.env['rh.visite.medicale'].browse(self._context['active_id'])
    #     visite_medical = self.env['rh.visite.medical.line'].create({
    #
    #         'employee_id': self.employee_id.id,
    #         'visite_medical_id': self.visite_medical_id.id,
    #         'date_visite_medicale': self.date_visite_medicale,
    #     })

    @api.model
    def _default_employees(self):
        return self.env['hr.employee'].search([])

    @api.model
    def detaille_formation(self):
        print('rec1')
        # for rec1 in self.employee_id_lines:
        #     print(rec1)
        #     if rec1.selection_employe_visite_medicale == True:
        #         visite_medical_Detail = self.env['rh.formation.line'].create({
        #             'employee_id': rec1.id,
        #            # 'visite_medical_id': self.visite_medical_id.id,
        #            #  'date_visite_medicale': self.date_visite_medicale,
        #         })



