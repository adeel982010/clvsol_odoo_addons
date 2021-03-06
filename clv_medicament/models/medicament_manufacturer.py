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

from odoo import api, fields, models


class MedicamentManufacturer(models.Model):
    _description = 'Medicament Manufacturer'
    _name = 'clv.medicament.manufacturer'
    _order = 'name'

    name = fields.Char(string='Manufacturer', required=True)

    code = fields.Char(string='Code')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Manufacturer must be unique!'),
        ('code_uniq',
         'UNIQUE (code)',
         u'Error! The Code must be unique!'),
    ]

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for manufacturer in self:
            result.append((manufacturer.id, '%s {%s}' % (manufacturer.name, manufacturer.code)))
        return result


class MedicamentManufacturerStr(models.Model):
    _description = 'Medicament Manufacturer String'
    _name = 'clv.medicament.manufacturer.str'
    _order = 'name'

    name = fields.Char(string='Manufacturer String', required=True)

    manufacturer_id = fields.Many2one(
        comodel_name='clv.medicament.manufacturer',
        string='Associated Manufacturer',
        help='Associated Medicament Manufacturer'
    )

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         u'Error! The Manufacturer String must be unique!'),
    ]
