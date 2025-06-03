{
    'name': 'Visitor Management',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'A comprehensive system to register, track, and manage visitors entering the premises.',
    'author': 'Bhargav Amarthaluru',
    'depends': ['base', 'website', 'contacts', 'frontdesk'],
    'data': [
        'security/ir.model.access.csv',
        'views/visitor_template.xml',
        'views/visitor_registration.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}
