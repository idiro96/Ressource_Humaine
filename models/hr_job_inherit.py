# -*- coding: utf-8 -*-
import math
# import time
#
# import schedule

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class HrJobInherited(models.Model):

    _inherit = "hr.job"

    nature_travail_id = fields.Many2one('rh.nature.travail')
    nature_poste = fields.Selection([('postesuperieure', 'Postesuperieure'),
                              ('fonctionsuperieure', 'Fonctionsuperieure'),
                              ], readonly=False)

