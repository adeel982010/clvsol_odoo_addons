# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
from functools import reduce

from odoo import models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class Document(models.Model):
    _name = 'clv.document'
    _inherit = 'clv.document', 'clv.external_sync.model'

    def _document_synchronize(
        self, sock, external_dbname, uid, external_user_pw,
        external_model, code
    ):

        external_object_fields = [
            'name', 'code', '__last_update',
        ]
        args = [('code', '=', code)]
        external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                        external_model, 'search_read',
                                        args,
                                        external_object_fields)

        external_object = external_objects[0]

        _logger.info(u'>>>>>>>>>>>>>>> %s %s', external_object, self)

        if self.name != external_object['name']:
            self.name = external_object['name']

        self.external_last_update = external_object['__last_update']
        self.external_sync = 'synchronized'

    def _document_external_sync(self, schedule):

        from time import time
        start = time()

        date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        upmost_last_update = False

        external_host = schedule.external_host_id.name
        external_dbname = schedule.external_host_id.external_dbname
        external_user = schedule.external_host_id.external_user
        external_user_pw = schedule.external_host_id.external_user_pw

        ExternalSyncModel = self.env['clv.external_sync.model']
        uid, sock, login_msg = ExternalSyncModel.external_sync_host_login(
            external_host,
            external_dbname,
            external_user,
            external_user_pw
        )
        schedule.external_sync_log = 'login_msg: ' + str(login_msg) + '\n\n'

        if uid is not False:

            Object = self.env[schedule.model]

            external_object_ids = sock.execute(external_dbname, uid, external_user_pw,
                                               schedule.external_model, 'search', [])
            _logger.info(u'%s %s', '>>>>>>>>>>', len(external_object_ids))

            local_objects = Object.search([
                ('external_id', '!=', False),
                ('external_sync', '!=', 'missing'),
            ])
            _logger.info(u'%s %s', '>>>>>>>>>>', len(local_objects))

            missing_count = 0
            for local_object in local_objects:
                if local_object.external_id not in external_object_ids:
                    missing_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>>>>>>', missing_count, local_object.code)
                    local_object.external_sync = 'missing'

            external_object_fields = sock.execute(external_dbname, uid, external_user_pw,
                                                  schedule.external_model, 'fields_get',
                                                  [], {'attributes': ['string', 'help', 'type']})
            _logger.info(u'%s %s', '>>>>>>>>>>', external_object_fields.keys())

            args = schedule.external_last_update_args()
            _logger.info(u'%s %s', '>>>>>>>>>>', args)

            external_object_fields = ['name', 'code', '__last_update', ]
            external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                            schedule.external_model, 'search_read',
                                            args,
                                            external_object_fields)

            _logger.info(u'%s %s', '>>>>>>>>>>', len(external_objects))

            reg_count = 0
            include_count = 0
            update_count = 0
            sync_count = 0
            sync_include_count = 0
            sync_update_count = 0
            for external_object in external_objects:

                reg_count += 1

                _logger.info(u'%s %s %s %s %s %s', '>>>>>>>>>>', reg_count,
                             external_object['id'], external_object['name'], external_object['code'],
                             external_object['__last_update'], )

                if upmost_last_update is False:
                    upmost_last_update = external_object['__last_update']
                else:
                    if external_object['__last_update'] > upmost_last_update:
                        upmost_last_update = external_object['__last_update']

                local_object = Object.search([
                    ('code', '=', external_object['code']),
                ])

                if local_object.id is False:

                    include_count += 1

                    values = {
                        'name': external_object['name'],
                        'code': external_object['code'],
                        'external_id': external_object['id'],
                        'external_last_update': external_object['__last_update'],
                        'external_sync': 'included',
                    }
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, values)
                    new_local_object = Object.create(values)
                    _logger.info(u'>>>>>>>>>>>>>>> %s %s', include_count, new_local_object)

                    if schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1
                        sync_include_count += 1

                        new_local_object._document_synchronize(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['code']
                        )

                else:

                    if external_object['__last_update'] > local_object.external_last_update and \
                       local_object.external_sync != 'included':

                        update_count += 1

                        local_object.external_sync = 'updated'

                    if (local_object.external_sync == 'included' or
                        local_object.external_sync == 'updated') and \
                       schedule.external_exec_sync is True and \
                       sync_count < schedule.external_max_sync:

                        sync_count += 1

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', sync_count, local_object)

                        if local_object.external_sync == 'included':
                            sync_include_count += 1

                        if local_object.external_sync == 'updated':
                            sync_update_count += 1

                        local_object._document_synchronize(
                            sock, external_dbname, uid, external_user_pw,
                            schedule.external_model, external_object['code']
                        )

            _logger.info(u'%s %s', '>>>>>>>>>> external_exec_sync: ', schedule.external_exec_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> external_max_sync: ', schedule.external_max_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> args: ', args)
            _logger.info(u'%s %s', '>>>>>>>>>> external_object_ids: ', len(external_object_ids))
            _logger.info(u'%s %s', '>>>>>>>>>> local_objects: ', len(local_objects))
            _logger.info(u'%s %s', '>>>>>>>>>> missing_count: ', missing_count)
            _logger.info(u'%s %s', '>>>>>>>>>> reg_count: ', reg_count)
            _logger.info(u'%s %s', '>>>>>>>>>> include_count: ', include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> update_count: ', update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_include_count: ', sync_include_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_update_count: ', sync_update_count)
            _logger.info(u'%s %s', '>>>>>>>>>> sync_count: ', sync_count)
            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> upmost_last_update: ', upmost_last_update)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.upmost_last_update = upmost_last_update
            schedule.external_sync_log +=  \
                'external_exec_sync: ' + str(schedule.external_exec_sync) + '\n' + \
                'external_max_sync: ' + str(schedule.external_max_sync) + '\n' + \
                'args: ' + str(args) + '\n\n' + \
                'external_object_ids: ' + str(len(external_object_ids)) + '\n' + \
                'local_objects: ' + str(len(local_objects)) + '\n' + \
                'missing_count: ' + str(missing_count) + '\n\n' + \
                'reg_count: ' + str(reg_count) + '\n' + \
                'include_count: ' + str(include_count) + '\n' + \
                'update_count: ' + str(update_count) + '\n' + \
                'sync_include_count: ' + str(sync_include_count) + '\n' + \
                'sync_update_count: ' + str(sync_update_count) + '\n' + \
                'sync_count: ' + str(sync_count) + '\n\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'upmost_last_update: ' + str(upmost_last_update) + '\n\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n'
