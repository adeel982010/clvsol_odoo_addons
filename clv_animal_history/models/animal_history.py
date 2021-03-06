# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import *

from odoo import api, fields, models


class AnimalHistory(models.Model):
    _description = 'Animal History'
    _name = 'clv.animal.history'
    _order = "sign_in_date desc"

    animal_id = fields.Many2one(
        comodel_name='clv.animal',
        string='Animal',
        required=False
    )
    sign_in_date = fields.Date(
        string='Sign in date',
        required=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d')
    )
    sign_out_date = fields.Date(
        string="Sign out date",
        required=False
    )

    category_ids = fields.Many2many(
        comodel_name='clv.animal.category',
        relation='clv_animal_category_animal_history_rel',
        column1='animal_history_id',
        column2='category_id',
        string='Categories'
    )
    category_names = fields.Char(
        string='Category Names',
        compute='_compute_category_names',
        store=True
    )
    category_names_suport = fields.Char(
        string='Category Names Suport',
        compute='_compute_category_names_suport',
        store=False
    )

    date_reference = fields.Date(string="Reference Date")
    age_reference = fields.Char(string='Reference Age')
    estimated_age = fields.Char(string='Estimated Age')

    tutor_id = fields.Many2one(
        comodel_name='clv.person',
        string='Tutor',
        ondelete='restrict'
    )

    address_id = fields.Many2one(
        comodel_name='clv.address',
        string='Address',
        ondelete='restrict'
    )

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    @api.depends('category_ids')
    def _compute_category_names(self):
        for r in self:
            r.category_names = r.category_names_suport

    @api.multi
    def _compute_category_names_suport(self):
        for r in self:
            category_names = False
            for category in r.category_ids:
                if category_names is False:
                    category_names = category.complete_name
                else:
                    category_names = category_names + ', ' + category.complete_name
            r.category_names_suport = category_names
            if r.category_names != category_names:
                record = self.env['clv.animal'].search([('id', '=', r.id)])
                record.write({'category_ids': r.category_ids})


class Animal(models.Model):
    _inherit = 'clv.animal'

    animal_history_ids = fields.One2many(
        comodel_name='clv.animal.history',
        inverse_name='animal_id',
        string='Animal History'
    )
