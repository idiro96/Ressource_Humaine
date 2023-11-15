# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class RHVisiteMedicalDetail(models.Model):
    _name = 'rh.visite.medical.line'

    id_visite_medical_detail = fields.Integer()
    date_visite_medicale = fields.Date()




