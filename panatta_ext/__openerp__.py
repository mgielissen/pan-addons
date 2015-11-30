# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Panatta EXT.',
    'version': '1.0',
    'author': "Jayesh joshi",
    'license': 'AGPL-3',
    'category': 'Others',
    'summary': 'email sent',
    'depends': [
        'base','crm','product','project' ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
    'security/panatta_security.xml',
    "security/ir.model.access.csv",
    'product_view.xml',
    'report_view.xml',
    'views/report_presupuesto_completo.xml',
    'views/report_propuesta_pedido.xml',
    ],
    'installable': True,
    'application': True,
}