# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrJobInherited(models.Model):
    _inherit = "hr.job"

    # nature_travail_id = fields.Many2one('rh.nature.travail')
    # nature_poste = fields.Selection([('postesuperieure', 'Postesuperieure'),
    #                           ('fonctionsuperieure', 'Fonctionsuperieure'),
    #                           ], readonly=False)
    nature_travail_id = fields.Many2one('rh.type.fonction')
    poste_organique = fields.Selection(selection=[('organique', 'منصب هيكلي'), ('squelaire', 'منصب عضوي')],
                                       readonly=False)
    max_employee = fields.Integer(store=True)

    @api.constrains('no_of_employee', 'max_employee')
    def _check_max_employee_limit(self):
        for job in self:
            if job.no_of_employee > job.max_employee:
                raise ValidationError("لا يجوز أن عدد الموظفين يتفوق عن الحد الأقصى المسموح به.")
