from odoo import models, fields, api, _


class RHTypeFile(models.Model):
    _name = 'rh.type.file'
    _rec_name = 'intitule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    intitule = fields.Char(track_visibility="onchange")
    intitule_fr = fields.Char(track_visibility="onchange")
    type_file = fields.Selection(
        [('indisponibilite', 'Indisponibilite'), ('sanction', 'Sanction'), ('formation', 'Formation'),
         ('finrelation', 'Fin Relation'), ('accidenttravail', 'Accident Travail'),
         ('controlemedicale', 'Contrôle Médicale'),
         ('employe', 'Employe'), ('promotion', 'Promotion'), ('avancement', 'Avancement'), ('autre', 'Autres')],
        default='draft', track_visibility="onchange")
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHTypeFile, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHTypeFile, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.type.file.sequence') or _('New')
        result = super(RHTypeFile, self).create(vals)
        return result
