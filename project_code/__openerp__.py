# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of project_code, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     project_code is free software: you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     project_code is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with project_code.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Project Code",
    "version": "1.0",
    "author": "ACSONE SA/NV",
    "maintainer": "ACSONE SA/NV",
    "website": "http://www.acsone.eu",
    "images": ["images/screenshot1.png",
               "images/screenshot2.png",
               "images/screenshot3.png"],
    "category": "Project Management",
    "complexity": "easy",
    "depends": ["project"],
    "description": """

A module for companies who like to reference projects by their code.

It has the following features:
 * the project code is made visible on project views (form, tree, filter)
 * the project and analytic account names are displayed as "code - name"
   (name_get)
 * quick search on project and analytic account include code (name_search)
""",
    "data": ["project_view.xml"],
    "demo": [],
    "test": [],
    "active": False,
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
}
