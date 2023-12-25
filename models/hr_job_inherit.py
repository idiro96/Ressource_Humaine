# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class HrJobInherited(models.Model):

    _inherit = "hr.job"

    type_job = fields.Selection([('fonctionnaire', 'موضف'),
                                ('contractuel', 'متعاقد'),('stagiaire', 'متربص'),],
                               string="Status", readonly=False,default='fonctionnaire')

