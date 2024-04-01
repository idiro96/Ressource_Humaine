from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class PromotionReport(models.AbstractModel):
    _name = 'report.ressource_humaine.promotion_report'

    @api.model
    def get_report_values(self, docids, data=None):
        promotion = self.env['rh.promotion'].browse(docids[0])

        promotion_lines = promotion.promotion_lines
        avance = []
        derniere_grille = []
        for rec in promotion_lines:
            # avancement_lines = avancement.avancement_lines
            employe_avancement_lines = self.env['rh.avancement.line'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_new_avancement', '<=', rec.date_promotion)],
                order='date_new_avancement desc', limit=1)
            if employe_avancement_lines:
                avance.append(employe_avancement_lines[0])
                print(employe_avancement_lines[0])
                for rec2 in employe_avancement_lines:
                    avancement_lines_grille3 = self.env['rh.avancement.line'].search(
                        [('employee_id', '=', rec2.employee_id.id),
                         ('grille_old_id', '=', rec2.grille_old_id.id)], order='date_avancement desc')
                    derniere_grille.append(avancement_lines_grille3[-1])


        line_date_old_promotion = {}
        for rec in promotion_lines:
            date_old_promotion_str = rec.date_grade
            if date_old_promotion_str:
                formatted_date_old_promotion = datetime.strptime(date_old_promotion_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_old_promotion[rec.id] = formatted_date_old_promotion
            else:
                line_date_old_promotion[rec.id] = ''

        line_date_ref_ouverture_examin = {}
        for rec in promotion:
            date_ref_ouverture_examin_str = rec.date_ref_ouverture_examin
            if date_ref_ouverture_examin_str:
                formatted_date_ref_ouverture_examin = datetime.strptime(date_ref_ouverture_examin_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_ref_ouverture_examin[rec.id] = formatted_date_ref_ouverture_examin
            else:
                line_date_ref_ouverture_examin[rec.id] = ''

        line_date_ref_promotion = {}
        for rec in promotion_lines:
            date_ref_promotion_str = rec.date_ref_promotion
            if date_ref_promotion_str:
                formatted_date_ref_promotion = datetime.strptime(date_ref_promotion_str,
                                                                        "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_ref_promotion[rec.id] = formatted_date_ref_promotion
            else:
                line_date_ref_promotion[rec.id] = ''

        line_date_grade = {}
        for rec in promotion_lines:
            date_grade_str = rec.date_grade
            if date_grade_str:
                formatted_date_grade = datetime.strptime(date_grade_str,
                                                                 "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_grade[rec.id] = formatted_date_grade
            else:
                line_date_grade[rec.id] = ''

        line_date_signature_av = {}
        for rec2 in avance:
            for rec in rec2:
                date_signature_str = rec.avancement_id.date_signature
                if date_signature_str:
                    formatted_date_signature = datetime.strptime(date_signature_str,
                                                             "%Y-%m-%d").strftime(
                        "%d-%m-%Y")
                    line_date_signature_av[rec.id] = formatted_date_signature
                else:
                    line_date_signature_av[rec.id] = ''

        line_date_new_avancement_av = {}
        for rec2 in avance:
            for rec in rec2:
                date_new_avancement_av_str = rec.date_new_avancement
                if date_new_avancement_av_str:
                    formatted_date_new_avancement_av = datetime.strptime(date_new_avancement_av_str,
                                                                 "%Y-%m-%d").strftime(
                        "%d-%m-%Y")
                    line_date_new_avancement_av[rec.id] = formatted_date_new_avancement_av
                else:
                    line_date_new_avancement_av[rec.id] = ''

        line_date_ref = {}
        # for rec in promotion_lines:
        #     date_ref_str = rec.date_ref
        #     if date_ref_str:
        #         formatted_date_ref = datetime.strptime(date_ref_str, "%Y-%m-%d").strftime(
        #             "%d-%m-%Y")
        #         line_date_ref[rec.id] = formatted_date_ref
        #     else:
        #         line_date_ref[rec.id] = ''

        line_date_promotion = {}
        for rec in promotion:
            date_promotion_str = rec.date_promotion
            if date_promotion_str:
                formatted_date_promotion = datetime.strptime(date_promotion_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_promotion[rec.id] = formatted_date_promotion
            else:
                line_date_promotion[rec.id] = ''

        line_date_decision_groupe = {}
        for rec in promotion:
            date_decision_groupe_str = rec.date_decision_groupe
            if date_promotion_str:
                formatted_date_decision_groupe = datetime.strptime(date_decision_groupe_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_decision_groupe[rec.id] = formatted_date_decision_groupe
            else:
                line_date_decision_groupe[rec.id] = ''

        line_date_examin_professionnel = {}
        for rec in promotion:
            date_examin_professionnel_str = rec.date_examin_professionnel
            if date_examin_professionnel_str:
                formatted_date_examin_professionnel= datetime.strptime(date_examin_professionnel_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_examin_professionnel[rec.id] = formatted_date_examin_professionnel
            else:
                line_date_examin_professionnel[rec.id] = ''

        line_date_effet_decision_groupe = {}
        for rec in promotion:
            date_effet_decision_groupe_str = rec.date_effet_decision_groupe
            if date_promotion_str:
                formatted_date_effet_decision_groupe = datetime.strptime(date_effet_decision_groupe_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_effet_decision_groupe[rec.id] = formatted_date_effet_decision_groupe
            else:
                line_date_effet_decision_groupe[rec.id] = ''

        line_date_new_grade = {}
        for rec in promotion_lines:
            date_new_grade_str = rec.date_new_grade
            if date_new_grade_str:
                formatted_date_new_grade = datetime.strptime(date_new_grade_str,
                                                                         "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_new_grade[rec.id] = formatted_date_new_grade
            else:
                line_date_new_grade[rec.id] = ''

        line_date_signature = {}
        for rec in promotion:
            date_signature_str = rec.date_signature
            if date_signature_str:
                formatted_date_signature = datetime.strptime(date_signature_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_signature[rec.id] = formatted_date_signature
            else:
                line_date_signature[rec.id] = '..................'

        line_date_new_promotion = {}
        for rec in promotion_lines:
            date_new_promotion_str = rec.date_new_grade
            if date_new_promotion_str:
                formatted_date_new_promotion = datetime.strptime(date_new_promotion_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_new_promotion[rec.id] = formatted_date_new_promotion
            else:
                line_date_new_promotion[rec.id] = ''

        line_date_code = {}
        for rec in promotion_lines:
            date_code_str = rec.employee_id.corps_id.filiere_id.date_code
            if date_code_str:
                formatted_date_code = datetime.strptime(date_code_str, "%Y-%m-%d").strftime(
                    "%d-%m-%Y")
                line_date_code[rec.id] = formatted_date_code
            else:
                line_date_code[rec.id] = ''

        line_date_nomination = {}
        for rec in promotion_lines:
            date_nomination_str = rec.employee_id.date_nomination
            if date_nomination_str :
                formatted_date_nomination = datetime.strptime(date_nomination_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                line_date_nomination[rec.id] = formatted_date_nomination
            else:
                line_date_nomination[rec.id] = ''


        line_date_ref_nomination = {}
        for rec in promotion_lines:
            date_ref_nomination_str = rec.employee_id.date_ref_nomination
            if date_ref_nomination_str:
                formatted_date_ref_nomination = datetime.strptime(date_ref_nomination_str, "%Y-%m-%d").strftime("%d-%m-%Y")
                line_date_ref_nomination[rec.id] = formatted_date_ref_nomination
            else:
                line_date_ref_nomination[rec.id] = ''



        report_data = {
            'promotion': promotion,
            'company': self.env.user.company_id,
            'promotion_lines': promotion_lines,
            'avance': avance,
            'grille_old': derniere_grille,
            'line_date_old_promotion': line_date_old_promotion,
            'line_date_ref_ouverture_examin': line_date_ref_ouverture_examin,
            'line_date_ref_promotion': line_date_ref_promotion,
            'line_date_signature_av': line_date_signature_av,
            'line_date_decision_groupe': line_date_decision_groupe,
            'line_date_effet_decision_groupe': line_date_effet_decision_groupe,
            'line_date_examin_professionnel': line_date_examin_professionnel,
            'line_date_new_avancement_av': line_date_new_avancement_av,
            'line_date_new_grade': line_date_new_grade,
            'line_date_grade': line_date_grade,
            'line_date_ref': line_date_ref,
            'line_date_promotion': line_date_promotion,
            'line_date_signature': line_date_signature,
            'line_date_new_promotion': line_date_new_promotion,
            'line_date_code': line_date_code,
            'line_date_nomination': line_date_nomination,
            'line_date_ref_nomination': line_date_ref_nomination,
        }

        return report_data
