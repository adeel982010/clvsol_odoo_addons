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

import logging
from datetime import *
import xlwt

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ModelExportSetUp(models.TransientModel):
    _name = 'clv.model_export.setup'

    def _default_model_export_ids(self):
        return self._context.get('active_ids')
    model_export_ids = fields.Many2many(
        comodel_name='clv.model_export',
        relation='clv_model_export_setup_rel',
        string='Model Exports',
        default=_default_model_export_ids)

    def _default_dir_path(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_dir_path()
    dir_path = fields.Char(
        string='Directory Path',
        required=True,
        help="Directory Path",
        default=_default_dir_path
    )

    def _default_file_name(self):
        ObjectModelExport = self.env['clv.object.model_export']
        return ObjectModelExport.model_export_file_name()
    file_name = fields.Char(
        string='File Name',
        required=True,
        help="File Name",
        default=_default_file_name
    )

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    @api.multi
    def do_model_export_setup(self):
        self.ensure_one()

        FileSystemDirectory = self.env['clv.file_system.directory']
        file_system_directory = FileSystemDirectory.search([
            ('directory', '=', self.dir_path),
        ])

        for model_export in self.model_export_ids:

            _logger.info(u'%s %s', '>>>>>', model_export.name)

            model_export.date_model_export = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            model_name = model_export.model_id.name
            label = ''
            if model_export.label is not False:
                label = '_' + model_export.label
            code = model_export.code
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')[2:]
            file_name = self.file_name\
                .replace('<model>', model_name)\
                .replace('_<label>', label)\
                .replace('<code>', code)\
                .replace('<timestamp>', timestamp)
            file_path = self.dir_path + '/' + file_name
            _logger.info(u'%s %s', '>>>>>>>>>>', file_path)

            book = xlwt.Workbook()

            sheet = book.add_sheet(file_name)
            row_nr = 0

            row = sheet.row(row_nr)
            col_nr = 0
            for field in model_export.model_export_field_ids:
                col_name = field.field_id.field_description
                if field.name is not False:
                    col_name = field.name
                row.write(col_nr, col_name)
                col_nr += 1

            book.save(file_path)

            model_export.directory_id = file_system_directory.id
            model_export.file_name = file_name
            model_export.stored_file_name = file_name

        return True
