# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
import csv
from io import StringIO

_logger = logging.getLogger(__name__)


class RHGrille(models.Model):
    _name = 'rh.grille'
    _rec_name = 'description_grille'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'

    code = fields.Char(readonly=True, default=lambda self: _('New'))
    date_publication_journal_officiel = fields.Date(track_visibility='onchange')
    date_application_provisoire = fields.Date(track_visibility='onchange')
    statut_applique = fields.Boolean()
    date_application_effective = fields.Date(track_visibility='onchange')
    num_decret_journal_officiel = fields.Char(track_visibility='onchange')
    description_grille = fields.Text(track_visibility='onchange')
    # a adapter selon les colonnes de la grille salariale de l'ENA
    # normalement une grille à un détail et le détail sera faite l'importation
    # specialite = fields.Char(string='specialite', required=True)
    # salaire = fields.Float(string='salaire', required=True)
    # specialite = fields.Char(required=True)
    # salaire = fields.Float(required=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, track_visibility='onchange')
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        vals['create_uid'] = self.env.user.id
        return super(RHGrille, self).create(vals)

    @api.multi
    def write(self, vals):
        vals['write_uid'] = self.env.user.id
        return super(RHGrille, self).write(vals)

    @api.model
    def check_date_application_provisoire_and_notify(self):

        records_to_notify = self.search([('date_application_provisoire', '=', fields.Date.today())])

        if records_to_notify:
            _logger.warning('Grille de salaire trouvée avec une date provisoire qui correspond à la date du jour')

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.code.sequence') or _('New')

        result = super(RHGrille, self).create(vals)
        return result

    @api.multi
    def importation_grille(self):
        print("en cours")
        # file_path = '/Program Files (x86)/Odoo 11.0/server/odoo/addons_cetic_invist/ressource_humaine/tmp/nouvelle_grille.csv'
        # with open(file_path, 'r') as file:
        #     data = file.read()
        # csv_data = csv.DictReader(StringIO(data))
        # for row in csv_data:
        #         self.create({
        #             'name': row['specialite'],
        #             'salaire': float(row['salaire']),
        #         })

    @api.multi
    def appliquer_grille(self):
        print("en cours")
