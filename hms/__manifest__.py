{
    'name': 'hms_patient',
    'summary': 'learning Odoo',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hms_views.xml',
        'views/department_views.xml',
        'views/doctors_views.xml',
        'views/patient_history_views.xml',
        'reports/report.xml',
        'reports/template.xml',


    ]
}