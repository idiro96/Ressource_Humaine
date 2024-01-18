# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHAvancement(models.Model):
    _name = 'rh.avancement'

    date_avancement = fields.Date()
    code = fields.Char()
    avancement_lines = fields.One2many('rh.avancement.line', inverse_name='avancement_id')
    avancement_lines_wizard = fields.One2many('rh.avancement.line.wizard', inverse_name='avancement_id')

    avancement_wizard = fields.Boolean(default=True)
    choisir_commission_lines = fields.One2many('rh.avancement.commission.line', 'avancement_id')
    # promotion_file_lines = fields.One2many('rh.file', 'promotion_id')

    @api.model
    def create(self, vals):
        for rec2 in self:
            rec2.avancement_wizard = False
            print(rec2.avancement_wizard)
            print('tttttttttetste1wizard')
        avancement = super(RHAvancement, self).create(vals)
        if avancement.avancement_lines_wizard and avancement.avancement_lines_wizard.ids:
            print(avancement.avancement_lines_wizard)
            for rec in avancement.avancement_lines_wizard:
                if rec.employee_id.nature_travail_id.code_type_fonction == 'fonction':

                    avance_line = self.env['rh.avancement.line'].create({
                    'employee_id': rec.employee_id.id,
                    'type_fonction_id': rec.employee_id.nature_travail_id.id,
                    'date_old_avancement': rec.date_avancement,
                    'grade_id': rec.grade_id.id,
                    'job_id': rec.job_id.id,
                    'date_avancement': avancement.date_avancement,
                    'avancement_id': avancement.id,
                    'groupe_old_id': rec.groupe_old_id.id,
                    'categorie_old_id': rec.categorie_old_id.id,
                    'echelon_old_id': rec.echelon_old_id.id,

                    'groupe_new_id': rec.groupe_new_id.id,
                    'categorie_new_id': rec.categorie_new_id.id,
                    'echelon_new_id': rec.echelon_new_id.id,
                    })
                    employee = self.env['hr.employee'].search(
                    [('id', '=', rec.employee_id.id)])
                    employee.write({
                        'date_avancement': avancement.date_avancement,
                    })
                    employee.write({
                        'groupe_id': rec.groupe_new_id.id,
                    })
                    employee.write({
                        'categorie_id': rec.categorie_new_id.id,
                    })
                    employee.write({
                        'echelon_id': rec.echelon_new_id.id,
                    })

                elif rec.employee_id.nature_travail_id.code_type_fonction == 'fonctionsuperieure':

                    avance_line = self.env['rh.avancement.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.employee_id.nature_travail_id.id,
                        'date_old_avancement': rec.date_avancement,
                        'grade_id': rec.grade_id.id,
                        'job_id': rec.job_id.id,
                        'date_avancement': avancement.date_avancement,
                        'avancement_id': avancement.id,
                        'categorie_old_id': rec.categorie_old_id.id,
                        'section_old_id': rec.section_old_id.id,
                        'echelon_old_id': rec.echelon_old_id.id,

                        'categorie_new_id': rec.categorie_new_id.id,
                        'section_new_id': rec.section_new_id.id,
                        'echelon_new_id': rec.echelon_new_id.id,
                    })
                    employee = self.env['hr.employee'].search(
                        [('id', '=', rec.employee_id.id)])
                    employee.write({
                        'date_avancement': avancement.date_avancement,
                    })
                    employee.write({
                        'section_new_id': rec.section_new_id.id,
                    })
                    employee.write({
                        'categorie_id': rec.categorie_new_id.id,
                    })
                    employee.write({
                        'echelon_id': rec.echelon_new_id.id,
                    })
                elif rec.employee_id.nature_travail_id.code_type_fonction == 'postesuperieure':
                    avance_line = self.env['rh.avancement.line'].create({
                        'employee_id': rec.employee_id.id,
                        'type_fonction_id': rec.employee_id.nature_travail_id.id,
                        'date_old_avancement': rec.date_avancement,
                        'grade_id': rec.grade_id.id,
                        'job_id': rec.job_id.id,
                        'date_avancement': avancement.date_avancement,
                        'avancement_id': avancement.id,
                        'groupe_old_id': rec.groupe_old_id.id,
                        'categorie_old_id': rec.categorie_old_id.id,
                        'echelon_old_id': rec.echelon_old_id.id,
                        'categorie_superieure_old_id': rec.categorie_superieure_old_id.id,
                        'section_superieure_old_id': rec.section_superieure_old_id.id,
                        'niveau_hierarchique_old_id': rec.niveau_hierarchique_old_id.id,

                        'groupe_new_id': rec.groupe_new_id.id,
                        'categorie_new_id': rec.categorie_new_id.id,
                        'echelon_new_id': rec.echelon_new_id.id,
                        'categorie_superieure_new_id': rec.categorie_superieure_new_id.id,
                        'section_superieure_new_id': rec.section_superieure_new_id.id,
                        'niveau_hierarchique_new_id': rec.niveau_hierarchique_new_id.id,
                    })

        return avancement

    @api.onchange('date_avancement')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        for rec1 in self:
            rec1.avancement_wizard = True
            print(rec1.avancement_wizard)
            print('tttttttttetste1wizardWizard')


        # record1 = self.env['droit.avencement'].browse(self._context['active_id'])
        domain = []
        employee = self.env['hr.employee'].search([])
        avancement_ligne_droit = self.env['rh.avancement.line.wizard'].search([])
        for record in avancement_ligne_droit:
            record.unlink()
        for rec2  in self:
            avancement_line = self.env['rh.avencement.droit'].search(
                [('date_avancement', '=', rec2.date_avancement),('sauvegarde', '=', True)],
                order='date_avancement desc')
        if avancement_line:
             for avance in avancement_line:
                    dateDebut_object = fields.Date.from_string(self.date_avancement)
                    dateDebut_object2 = fields.Date.from_string(avance.date_avancement)
                    difference = (
                                             dateDebut_object.year - dateDebut_object2.year) * 12 + dateDebut_object.month - dateDebut_object2.month
                    # difference = dateDebut_object - dateDebut_object2
                    print(avance.employee_id.id)
                    print('difference')

                    if avance.type_fonction_id.code_type_fonction == 'fonction':
                        self.env['rh.avancement.line.wizard'].create({
                            'employee_id': avance.employee_id.id,
                            'type_fonction_id': avance.type_fonction_id.id,
                            'date_old_avancement': avance.date_avancement,
                            'grade_id': avance.grade_id.id,
                            'job_id': avance.job_id.id,
                            'groupe_old_id': avance.groupe_old_id.id,
                            'categorie_old_id': avance.categorie_old_id.id,
                            'echelon_old_id': avance.echelon_old_id.id,

                            'groupe_new_id': avance.groupe_new_id.id,
                            'categorie_new_id': avance.categorie_new_id.id,
                            'echelon_new_id': avance.echelon_new_id.id

                        })
                    elif avance.type_fonction_id.code_type_fonction == 'fonctionsuperieure':
                        self.env['rh.avancement.line.wizard'].create({
                            'employee_id': avance.employee_id.id,
                            'type_fonction_id': avance.type_fonction_id.id,
                            'date_old_avancement': avance.date_avancement,
                            'grade_id': avance.grade_id.id,
                            'job_id': avance.job_id.id,
                            'categorie_old_id': avance.categorie_old_id.id,
                            'section_old_id': avance.section_old_id.id,
                            'echelon_old_id': avance.echelon_old_id.id,


                            'categorie_new_id': avance.categorie_new_id.id,
                            'section_new_id': avance.section_new_id.id,
                            'echelon_new_id': avance.echelon_new_id.id,

                        })
                    elif avance.type_fonction_id.code_type_fonction == 'postesuperieure':
                        self.env['rh.avancement.line.wizard'].create({
                            'employee_id': avance.employee_id.id,
                            'type_fonction_id': avance.type_fonction_id.id,
                            'date_old_avancement': avance.date_avancement,
                            'grade_id': avance.grade_id.id,
                            'job_id': avance.job_id.id,
                            'groupe_old_id': avance.groupe_old_id.id,
                            'categorie_old_id': avance.categorie_old_id.id,
                            'echelon_old_id': avance.echelon_old_id.id,
                            'categorie_superieure_old_id': avance.categorie_superieure_old_id.id,
                            'section_superieure_old_id': avance.section_superieure_old_id.id,
                            'niveau_hierarchique_old_id': avance.niveau_hierarchique_old_id.id,

                            'groupe_new_id': avance.groupe_new_id.id,
                            'categorie_new_id': avance.categorie_new_id.id,
                            'echelon_new_id': avance.echelon_new_id.id,
                            'categorie_superieure_new_id': avance.categorie_superieure_new_id.id,
                            'section_superieure_new_id': avance.section_superieure_new_id.id,
                            'niveau_hierarchique_new_id': avance.niveau_hierarchique_new_id.id
                        })

        self.avancement_lines_wizard = self.env['rh.avancement.line.wizard'].search([])

        return {
                'type': 'ir.actions.act_window',
                'target': 'new',
                'name': 'Avancement',
                'view_mode': 'form',
                'res_model': 'rh.avancement',
            }

    def choisir_commission(self):

        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Commission Avancement',
            'view_mode': 'form',
            'res_model': 'commission.avancement',
        }


