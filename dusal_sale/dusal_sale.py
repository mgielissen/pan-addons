# -*- coding: utf-8 -*-
##############################################################################
#
#    Addon for Odoo sale by Dusal.net
#    Copyright (C) 2015 Dusal.net Almas
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


import logging

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.modules.module import get_module_resource
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
from openerp import models


class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
        'print_product_image':fields.boolean('Print product image', readonly=False, select=True, help="If this checkbox checked then print product images on Sales order & Quotation"),
        'image_size': fields.selection([('small', 'Small'), ('medium', 'Medium'), ('original', 'Original')], 'Image sizes', help="Choose an image size here", select=True),
        'print_line_number':fields.boolean('Print line number', readonly=False, select=True, help="Print line number on Sales order & Quotation"),
    }
    _defaults = {   'print_product_image': True, 
                    'image_size': 'small',
                    'print_line_number': False, 
                    }
    
class sale_order_line(models.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    _columns = {
        'product_image_small': fields.related('product_id', 'image_small', type='binary', string='Image small'),
        'product_image_medium': fields.related('product_id', 'image_medium', type='binary', string='Image medium'),
        'product_image': fields.related('product_id', 'image', type='binary', string='Image'),
    }
