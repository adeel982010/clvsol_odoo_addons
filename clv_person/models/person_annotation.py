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

from openerp import fields, models


class PersonAnotation(models.Model):
    _description = 'Person Annotation'
    _name = 'clv.person.annotation'
    _inherit = 'clv.object.annotation'

    person_id = fields.Many2one(
        comodel_name='clv.person',
        string='Person',
        ondelete='cascade'
    )


class Person(models.Model):
    _inherit = "clv.person"

    annotation_ids = fields.One2many(
        comodel_name='clv.person.annotation',
        inverse_name='person_id',
        string='Annotations'
    )