# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Lab Test',
    'summary': 'Lab Test Module used by CLVsol Solutions.',
    'version': '3.0.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'images': [],
    'depends': [
        'clv_base',
        'clv_file_system',
    ],
    'data': [
        'security/lab_test_security.xml',
        'security/ir.model.access.csv',
        'views/lab_test_type_view.xml',
        'views/lab_test_type_log_view.xml',
        'views/lab_test_request_view.xml',
        'views/lab_test_request_log_view.xml',
        'views/lab_test_report_view.xml',
        'views/lab_test_report_log_view.xml',
        'views/lab_test_result_view.xml',
        'views/lab_test_result_log_view.xml',
        'views/lab_test_unit_view.xml',
        'views/lab_test_criterion_view.xml',
        'views/global_tag_view.xml',
        'views/lab_test_result_file_system_view.xml',
        'views/lab_test_report_file_system_view.xml',
        'views/referenceable_model_view.xml',
        'wizard/lab_test_request_updt_view.xml',
        'wizard/lab_test_result_updt_view.xml',
        'wizard/lab_test_report_updt_view.xml',
        'wizard/lab_test_result_edit_view.xml',
        'wizard/lab_test_report_edit_view.xml',
        'wizard/lab_test_report_get_results_view.xml',
        'wizard/lab_test_result_copy_to_report_view.xml',
        'wizard/lab_test_type_duplicate_view.xml',
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
