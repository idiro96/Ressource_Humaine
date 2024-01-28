

from odoo import models, fields, api, _



class RHTypeFile(models.Model):
    _name = 'rh.type.file'
    _rec_name = 'intitule'


    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule = fields.Char()
    type_file = fields.Selection(
        [('indisponibilite', 'Indisponibilite'), ('sanction', 'Sanction'), ('formation', 'Formation'), ('finrelation', 'Fin Relation'),('accidenttravail', 'Accident Travail'),('controlemedicale', 'Contrôle Médicale'),('employe', 'Employe'),('promotion', 'Promotion'),('avancement', 'Avancement'),('autre', 'Autres')], default='draft')






