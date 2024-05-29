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
    old_grille_id = fields.Many2one('rh.grille', track_visibility='onchange')
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


    def update_employee(self):
        print('rabah')
        employees = self.env['hr.employee'].search([])
        for record in self:
            if employees:
                for rec in employees:
                    grille = self.env['rh.grille'].search(
                        [('old_grille_id', '=', rec.grille_id.id)])
                    if grille:
                        rec.write({
                            'grille_id': record.id,
                        })
                    type_fonction = self.env['rh.type.fonction'].search([('id', '=', rec.nature_travail_id.id)])
                    if type_fonction.code_type_fonction == 'fonction':
                        groupe = self.env['rh.groupe'].search(
                            [('old_groupe_id', '=', rec.groupe_id.id),('grille_id', '=', record.id)],limit=1)
                        if groupe:
                            rec.write({
                                'groupe_id': groupe.id,
                            })
                            categorie = self.env['rh.categorie'].search(
                                [('old_categorie_id', '=', rec.categorie_id.id),('grille_id', '=', record.id)],limit=1)
                            if categorie:
                                rec.write({
                                    'categorie_id': categorie.id,
                                })
                                rec.write({
                                    'indice_minimal': categorie.Indice_minimal,
                                })
                                echelon = self.env['rh.echelon'].search(
                                    [('old_echelon_id', '=', rec.echelon_id.id),('grille_id', '=', record.id)],limit=1)
                                if echelon:
                                    rec.write({
                                        'echelon_id': echelon.id,
                                    })
                                    rec.write({
                                        'point_indiciare': echelon.indice_echelon,
                                    })
                                    rec.write({
                                        'total_indice': echelon.indice_echelon + categorie.Indice_minimal,
                                    })
                                    rec.write({
                                        'wage': categorie.Indice_minimal * 45 + echelon.indice_echelon * 45,
                                    })
                                    if rec.chef_bureau:
                                        niveau_chef_Bureau = self.env['rh.niveau.hierarchique.chef.bureau'].search(
                                            [('old_chef_bureau_id', '=', rec.niveau_hirerachique_chef_Bureau.id), ('grille_id', '=', record.id)],
                                            limit=1)
                                        if niveau_chef_Bureau:
                                            rec.write({
                                                'niveau_hirerachique_chef_Bureau': niveau_chef_Bureau.id,
                                            })
                                            rec.write({
                                                'bonification_indiciaire': rec.niveau_hirerachique_chef_Bureau.bonification_indiciaire,
                                            })
                                            rec.write({
                                                'wage': (categorie.Indice_minimal * 45 + echelon.indice_echelon * 45) + rec.niveau_hirerachique_chef_Bureau.bonification_indiciaire,
                                            })

                    if type_fonction.code_type_fonction == 'fonctionsuperieure':
                        categorie = self.env['rh.categorie'].search(
                            [('old_categorie_id', '=', rec.categorie_id.id),('grille_id', '=', record.id)],limit=1)
                        if categorie:
                            rec.write({
                                'categorie_id': categorie.id,
                            })
                            section = self.env['rh.section'].search(
                                [('old_section_id', '=', rec.section_id.id),('grille_id', '=', record.id)],limit=1)
                            rec.write({
                                'section_id': section.id,
                            })
                            rec.write({
                                'indice_base': section.indice_base,
                            })

                            echelon = self.env['rh.echelon'].search(
                                [('old_echelon_id', '=', rec.echelon_id.id),('grille_id', '=', record.id)],limit=1)
                            if echelon:
                                rec.write({
                                    'echelon_id': echelon.id,
                                })
                                rec.write({
                                    'point_indiciare': echelon.indice_echelon,
                                })
                                rec.write({
                                    'total_indice': echelon.indice_echelon + section.indice_base,
                                    })
                                rec.write({
                                    'wage': section.indice_base * 45 + echelon.indice_echelon,
                                })
                    if type_fonction.code_type_fonction == 'contractuel':
                        categorie = self.env['rh.categorie'].search(
                            [('old_categorie_id', '=', rec.categorie_id.id),('grille_id', '=', record.id)],limit=1)
                        if categorie:
                            rec.write({
                                'categorie_id': categorie.id,
                            })
                            rec.write({
                                'indice_minimal': categorie.Indice_minimal,
                            })

                            rec.write({
                                'total_indice': categorie.Indice_minimal,
                                })
                            rec.write({
                                'wage': categorie.Indice_minimal * 45,
                            })
        grades = self.env['rh.grade'].search([])
        for recor  in grades:
            categories = self.env['rh.categorie'].search(
                [('old_categorie_id', '=', recor.categorie_id.id)], limit=1)
            if categories:
                recor.write({
                    'categorie_id': categories.id,
                })
                print('moi')

    @api.model
    def create(self, vals):

        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('rh.code.sequence') or _('New')
        grille = self.env['rh.grille'].search([],limit=1, order='create_date desc')
        vals['old_grille_id'] = grille.id
        result = super(RHGrille, self).create(vals)

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
                        'old_groupe_id': record.id,
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
                                'old_categorie_id': cat.id,
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
                                        'old_echelon_id': ech.id,
                                    })
            niveau_hierarchique_chef_bureau = self.env['rh.niveau.hierarchique.chef.bureau'].search([('grille_id', '=', grille.id)])
            if niveau_hierarchique_chef_bureau:
                for chefB in niveau_hierarchique_chef_bureau:
                    chefB_new = self.env['rh.niveau.hierarchique.chef.bureau'].create({
                        'intitule': chefB.intitule,
                        'grille_id': result.id,
                        'bonification_indiciaire': chefB.bonification_indiciaire,
                        'indice_echelon': ech.indice_echelon,
                        'old_chef_bureau_id': chefB.id,
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
                        'old_categorie_id': catsup.id,
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
                                'old_section_id': sect.id,
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
                                        'old_echelon_id': ech_sect.id,
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
