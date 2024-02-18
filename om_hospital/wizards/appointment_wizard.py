from odoo import models, api , fields

class NomDeLaClasse(models.TransientModel):
    _name = "appointment.wizard"

    name = fields.Many2one('hospital.patient', string="Nom")
    note = fields.Text(string='Notes')

