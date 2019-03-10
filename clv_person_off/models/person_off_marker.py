# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PersonMarker(models.Model):
    _inherit = 'clv.person.marker'

    person_off_ids = fields.Many2many(
        comodel_name='clv.person_off',
        relation='clv_person_off_marker_rel',
        column1='marker_id',
        column2='person_off_id',
        string='Persons (Off)'
    )


class PersonOff(models.Model):
    _inherit = "clv.person_off"

    marker_ids = fields.Many2many(
        comodel_name='clv.person.marker',
        relation='clv_person_off_marker_rel',
        column1='person_off_id',
        column2='marker_id',
        string='Markers'
    )
    marker_names = fields.Char(
        string='Marker Names',
        compute='_compute_marker_names',
        store=True
    )

    @api.depends('marker_ids')
    def _compute_marker_names(self):
        for r in self:
            marker_names = False
            for marker in r.marker_ids:
                if marker_names is False:
                    marker_names = marker.name
                else:
                    marker_names = marker_names + ', ' + marker.name
            r.marker_names = marker_names
