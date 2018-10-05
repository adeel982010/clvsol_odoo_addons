# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'External Sync',
    'summary': 'External Sync Module used by CLVsol Solutions.',
    'version': '4.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_global_log',
    ],
    'data': [
        'security/external_sync_security.xml',
        'security/ir.model.access.csv',
        'views/external_sync_host_view.xml',
        'views/external_sync_host_log_view.xml',
        'views/external_sync_template_view.xml',
        'views/external_sync_template_log_view.xml',
        'views/external_sync_schedule_view.xml',
        'views/external_sync_schedule_log_view.xml',
        'views/external_sync_object_field_view.xml',
        'wizard/external_sync_template_mass_edit_view.xml',
        'wizard/external_sync_schedule_exec_view.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
