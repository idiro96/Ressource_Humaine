# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHPromotion(models.Model):
    _name = 'rh.promotion'

    date_examin_professionnel = fields.Date()
    date_promotion = fields.Date()
    code = fields.Char()
    promotion_lines = fields.One2many('rh.promotion.line', inverse_name='promotion_id')
    promotion_file_lines = fields.One2many('rh.file', 'promotion_id')
    promotion_lines_wizard = fields.One2many('rh.promotion.line.wizard', inverse_name='promotion_id')

    avancement_wizard = fields.Boolean(default=True)

    type_fonction_id = fields.Many2one('rh.type.fonction')
    grade_id = fields.Many2one('rh.grade')
    date_grade = fields.Date()

    grade_new_id = fields.Many2one('rh.grade')
    date_new_grade = fields.Date()
    choisir_commission_lines = fields.One2many('rh.promotion.commission.line', 'promotion_id')

    @api.model
    def create(self, vals):
        for rec2 in self:
            rec2.avancement_wizard = False

        promotion = super(RHPromotion, self).create(vals)
        if promotion.promotion_lines_wizard and promotion.promotion_lines_wizard.ids:
            for rec in promotion.promotion_lines_wizard:
                if rec.employee_id.nature_travail_id.code_type_fonction == 'fonction':

                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'date_examin_professionnel': self.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade

                    })

                    employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    corps = self.env['rh.grade'].search([('corps_id', '=', rec.grade_new_id.id)])
                    if corps:
                        employee.write({'corps_id': corps.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})

                elif rec.employee_id.nature_travail_id.code_type_fonction == 'fonctionsuperieure':

                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'date_examin_professionnel': self.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade

                    })
                    employee = self.env['rh.employee'].search([('id', '=', rec.employee_id.id)])
                    corps = self.env['hr.grade'].search([('corps_id', '=', rec.grade_new_id.id)])
                    if corps:
                        employee.write({'corps_id': corps.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'postesuperieure':
                    promo_line = self.env['rh.promotion.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.type_fonction_id.id,
                        'date_examin_professionnel': self.date_examin_professionnel,
                        'promotion_id': promotion.id,
                        'grade_id': rec.grade_id.id,
                        'date_grade': rec.date_grade,
                        'grade_new_id': rec.grade_new_id.id,
                        'date_new_grade': rec.date_new_grade

                    })
                    employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                    corps = self.env['rh.grade'].search([('corps_id', '=', rec.grade_new_id.id)])
                    if corps:
                        employee.write({'corps_id': corps.id})
                    employee.write({'grade_id': rec.grade_new_id.id})
                    employee.write({'date_grade': rec.date_new_grade})


        return promotion



    @api.onchange('date_promotion')
    def _onchange_date_promotion(self):
        """ Update the number_of_days. """
        for rec1 in self:
            rec1.promotion_wizard = True

        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        promotion_ligne_droit = self.env['rh.promotion.line.wizard'].search([])
        for record in promotion_ligne_droit:
            record.unlink()
        promotion_line = self.env['hr.employee'].search(
                [('date_grade', '<=', self.date_promotion)],
                order='date_grade desc')
        if promotion_line:
            for promo in promotion_line:
                dateDebut_object = fields.Date.from_string(self.date_promotion)
                dateDebut_object2 = fields.Date.from_string(promo.date_grade)
                difference = (
                                        dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                print(difference)
                print('tttttttttetste1wizardWizard')

                if difference >= 12:
                        self.env['rh.promotion.line.wizard'].create({
                            'employee_id': promo.id,
                            'type_fonction_id': promo.nature_travail_id.id,
                            'grade_id': promo.grade_id.id,
                            'date_grade': promo.date_grade,
                            'grade_new_id': None,
                            'date_new_grade': self.date_promotion,

                        })
                # elif difference >= 12 and promotion_line.nature_travail_id.code_type_fonction == 'fonctionsuperieure':
                #         self.env['rh.promotion.line.wizard'].create({
                #             'employee_id': promotion_line.id,
                #             'type_fonction_id': promotion_line.nature_travail_id.id,
                #             'grade_id': promotion_line.grade_id.id,
                #             'date_grade': promotion_line.date_grade,
                #             'grade_new_id': None,
                #             'date_new_grade': self.date_promotion,
                #
                #         })
                # elif difference >= 12 and promotion_line.nature_travail_id.code_type_fonction == 'postesuperieure':
                #         self.env['rh.promotion.line.wizard'].create({
                #             'employee_id': promotion_line.id,
                #             'type_fonction_id': promotion_line.nature_travail_id.id,
                #             'grade_id': promotion_line.grade_id.id,
                #             'date_grade': promotion_line.date_grade,
                #             'grade_new_id': None,
                #             'date_new_grade': self.date_promotion,
                #
                #         })

        self.promotion_lines_wizard = self.env['rh.promotion.line.wizard'].search([])

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Promotion',
            'view_mode': 'form',
            'res_model': 'rh.promotion',
        }
    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Commission Promotion',
            'view_mode': 'form',
            'res_model': 'commission.promotion',
        }




