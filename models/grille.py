# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
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

    @api.multi
    def unlink(self):
        raise UserError(
            "لا يمكنك حذف هذا التسجيل")
        return super(RHGrille, self).unlink()

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
        grille = self.env['rh.grille'].search([('description_grille', '=', 54)])
        for rec in grille:
            print('test')
            print(rec)
            groupe = self.env['rh.groupe'].search([('grille_id', '=', rec.id)])
            if groupe:
                for record in groupe:
                    print('test2')
                    print(record)
                    groupe_new = self.env['rh.groupe'].create({
                        'name': record.name,
                        'description': record.description,
                        'grille_id': result.id,
                    })
                    categorie = self.env['rh.categorie'].search([('groupe_id', '=', record.id)])
                    if categorie:
                        for cat in categorie:
                            categorie_new = self.env['rh.categorie'].create({
                                'intitule': cat.intitule,
                                'description': cat.description,
                                'Indice_minimal': cat.Indice_minimal,
                                'type_fonction_id': cat.type_fonction_id.id,
                                'grille_id': result.id,
                                'groupe_id': groupe_new.id,
                            })
                            echelon = self.env['rh.echelon'].search([('categorie_id', '=', cat.id)])
                            if echelon:
                                for ech in echelon:
                                    echelon_new = self.env['rh.echelon'].create({
                                        'intitule': ech.intitule,
                                        'type_fonction': ech.type_fonction.id,
                                        'grille_id': result.id,
                                        'categorie_id': categorie_new.id,
                                        'indice_echelon': ech.indice_echelon,
                                    })

            categorie_sup = self.env['rh.categorie'].search([('grille_id', '=', rec.id),('groupe_id', '=', None)])
            if categorie_sup:
                for catsup in categorie_sup:
                    categorie_sup_new = self.env['rh.categorie'].create({
                        'intitule': catsup.intitule,
                        'description': catsup.description,
                        'Indice_minimal': catsup.Indice_minimal,
                        'type_fonction_id': catsup.type_fonction_id.id,
                        'grille_id': result.id,
                    })
                    section = self.env['rh.section'].search(
                        [('categorie_id', '=', catsup.id)])
                    if section:
                        for sect in section:
                            section_new = self.env['rh.section'].create({
                                'intitule': sect.intitule,
                                'description': sect.description,
                                'indice_base': sect.indice_base,
                                'categorie_id': categorie_sup_new.id,
                                'grille_id': result.id,
                            })
                            echelon_section = self.env['rh.echelon'].search([('section', '=', sect.id)])
                            if echelon_section:
                                for ech_sect in echelon_section:
                                    echelon_sect_new = self.env['rh.echelon'].create({
                                        'intitule': ech_sect.intitule,
                                        'type_fonction': ech_sect.type_fonction.id,
                                        'grille_id': result.id,
                                        'categorie_id': categorie_sup_new.id,
                                        'section': section_new.id,
                                        'indice_echelon': ech_sect.indice_echelon,
                                    })

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
