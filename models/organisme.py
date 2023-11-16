# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHOrganisme(models.Model):
    _name = 'rh.organisme'

    code_organisme = fields.Char()
    rs_organisme = fields.Char()
    adresse_organisme = fields.Char()




