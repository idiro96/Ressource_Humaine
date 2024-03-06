# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrJobInherited(models.Model):
    _inherit = "hr.job"

    # nature_travail_id = fields.Many2one('rh.nature.travail')
    # nature_poste = fields.Selection([('postesuperieure', 'Postesuperieure'),
    #                           ('fonctionsuperieure', 'Fonctionsuperieure'),
    #                           ], readonly=False)
    nature_travail_id = fields.Many2one('rh.type.fonction')
    poste_organique = fields.Selection(selection=[('organique', 'منصب هيكلي'), ('squelaire', 'منصب عضوي')],
                                       readonly=False)
    max_employee = fields.Integer(default=1, store=True)
    nombre_de_postes_vacants = fields.Integer(compute='_compute_nombre_de_postes_vacants', store=True, )
    code_type_fonction = fields.Char(related='nature_travail_id.code_type_fonction',
                                     string='Code Type Fonction', store=True)
    methode_embauche = fields.Selection([('recrutement', 'Recrutement'), ('transfert', 'Transfert'),
                                         ('detachement', 'Detachement'), ], related='employee_ids.methode_embauche')

    # @api.constrains('no_of_employee', 'max_employee')
    # def _check_max_employee_limit(self):
    #     for job in self:
    #         if job.no_of_employee > job.max_employee:
    #             raise ValidationError("لا يجوز أن عدد الموظفين يتفوق عن الحد الأقصى المسموح به")

    @api.depends('max_employee', 'no_of_employee')
    def _compute_nombre_de_postes_vacants(self):
        for job in self:
            job.nombre_de_postes_vacants = job.max_employee - job.no_of_employee

    @api.multi
    def unlink(self):
        raise UserError(
            "Vous ne pouvez pas supprimer cet enregistrement")
        return super(HrJobInherited, self).unlink()

    @api.depends('no_of_recruitment', 'employee_ids.job_id', 'employee_ids.active', 'employee_ids.methode_embauche')
    def _compute_employees(self):
        for job in self:
            # Updated query to consider all values of 'methode_embauche'
            query = """
                    SELECT job_id, COUNT(*) AS job_id_count
                    FROM hr_employee
                    WHERE job_id = %s AND methode_embauche = %s
                    GROUP BY job_id
                """
            job_id = job.id if job.id else None  # Use None if job.id is None (NewId)
            self.env.cr.execute(query, (job_id, 'recrutement'))
            result = self.env.cr.dictfetchone()

            if result is not None:
                job.no_of_employee = result.get('job_id_count', 0)
            else:
                job.no_of_employee = 0

    @api.multi
    def _update_employee_count(self, old_methode_embauche, new_methode_embauche):
        query = """
                UPDATE hr_employee
                SET job_id = %s
                WHERE job_id = %s AND methode_embauche = %s
            """
        for job in self:
            self.env.cr.execute(query, (job.id, job.id, old_methode_embauche))
            self.env.cr.execute(query, (job.id, job.id, new_methode_embauche))

    @api.onchange('methode_embauche')
    def _onchange_methode_embauche(self):
        old_methode_embauche = self._origin.methode_embauche
        new_methode_embauche = self.methode_embauche
        if old_methode_embauche != new_methode_embauche:
            self._update_employee_count(old_methode_embauche, new_methode_embauche)