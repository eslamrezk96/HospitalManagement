# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'summary': """ Module for managing the hospitals """,
    'category': 'Extra Tools',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'data/sequence.xml',
        'data/cron.xml',
        'wizard/create_appointment.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
