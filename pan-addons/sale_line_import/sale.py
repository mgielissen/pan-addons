# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: julio (julio@vauxoo.com)
############################################################################
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

from openerp.osv import osv
from openerp.tools.translate import _

import csv
import cStringIO
import openerp.tools as tools


class sale_order(osv.Model):
    _inherit = 'sale.order'

    def import_data_line(self, cr, uid, ids, fdata, favalidate, context={}):
        order = self.pool.get('sale.order').browse(cr, uid, ids)
        obj_prod = self.pool.get('product.product')
        saleorderline_obj = self.pool.get('sale.order.line')
        input = cStringIO.StringIO(fdata)
        input.seek(0)
        print '------ids-------------',ids
        data = list(csv.reader(input, quotechar='"' or '"', delimiter=','))
        print '------data-------------',data
        print '------[0]-------------',data[0]
#        csv_formate = ['Reference','Quantity','unit price']

        for dat in data[1:]:
            dat.append(ids)
            print '------dat-------------',dat
            sku = dat[0].strip('')
            prod_id = obj_prod.search(cr,uid,[('default_code','=',sku)])
            if len(prod_id):
                product= obj_prod.browse(cr,uid,prod_id[0])
                orderlinevals = {
                'order_id' : ids,
                'product_uom_qty' : int(dat[1]),
                'product_uom' : product.product_tmpl_id.uom_id.id,
                'price_unit' : float(dat[2]),
                'name':product.product_tmpl_id.name,
                'invoiced' : False,
                'state' : 'draft',
                'product_id' : product.id,
#                'tax_id' : [],
                }
                get_lineid = saleorderline_obj.search(cr,uid,[('product_id','=', product.id),('order_id','=', ids)])
                if not get_lineid: 
                    saleorderlineid = saleorderline_obj.create(cr,uid,orderlinevals)
                cr.commit()
#            try:
#                prod_name = dat[list_prod]
#            except:
#                prod_name = False
#            print '------prod_name-------------',prod_name
#            
#            context.update({'partner_id': order.partner_id.id})
#            print '------context-------------',context
#            prod_name_search = prod_name and self.pool.get(
#                'product.product').name_search(cr, uid, prod_name,
#                                               context=context) or False
#            print '------prod_name_search-------------',prod_name_search                                   
#            prod_id = prod_name_search and prod_name_search[0][0] or False
#            print '------prod_id-------------',prod_id 
#            lines = prod_id and self.pool.get(
#                'sale.order.line').product_id_change(cr, uid, [],
#                                                     order.pricelist_id.id,
#                                                     prod_id, qty=0, uom=False,
#                                                     qty_uos=0, uos=False,
#                                                     name='',
#                                                     partner_id=order.partner_id.id,
#                                                     lang=False,
#                                                     update_tax=True,
#                                                     date_order=False,
#                                                     packaging=False,
#                                                     fiscal_position=False,
#                                                     flag=False,).get('value',
#                                                                      False)\
#                or {}
#            print'lines--------------',lines
#            print'prod_name-----vvvv---------',prod_name
#            if not lines and prod_name:
#                not_products.append(prod_name)
#            if not prod_name:
#                self.pool.get('sale.order.line').import_data(
#                    cr, uid, data2, [dat], 'init', '')
#            for lin in range(len(lines.keys())):
#                print'lines.keys-----vvvv---------',lines.keys()[lin]
#                if lines.keys()[lin] not in data[0]:
#                    if lines.keys()[lin] in ('tax_id', 'product_uom',
#                                             'product_packaging'):
#                        field_val = str(lines.keys()[lin])
#                        field_val = field_val + '.id'
#                        data2.append(field_val)
#                        vals_many = str(lines[lines.keys()[lin]]).replace(
#                            '[', '').replace(']', '').replace('False', '')
#                        dat.append(vals_many)
#                    else:
#                        print'data2-----vvvv---------',lines.keys()[lin]
#                        print'dat-----vvvv---------',lines[lines.keys()[lin]]
#                        data2.append(lines.keys()[lin])
#                        dat.append(lines[lines.keys()[lin]])
#                else:
#                    val_str = dat[data[0].index(lines.keys()[lin])]
#                    val_str_2 = lines[lines.keys()[lin]]
#                    print'val_str_2-----vvvv---------',val_str_2
#                    print'val_str-----vvvv---------',val_str
#                    print'else-----vvvv---------',lines.keys()[lin]
#                    if lines.keys()[lin] == 'product_uom':
#                        val_str_2 = self.pool.get(
#                            'product.uom').browse(cr, uid, val_str_2).name
#                        print'else --if-----vvvv---------',val_str_2
#                        val_str = dat[data[0].index(lines.keys()[lin])]
#                        print'val_str----else---------',val_str
#                    if lines.keys()[lin] == 'price_unit':
#                        product_price = []
#                        product_price.append(prod_name)
#                        val_str = float(dat[data[0].index(lines.keys()[lin])])
#                        val_str_2 = float(lines[lines.keys()[lin]])
#                        if tools.ustr(val_str) != tools.ustr(val_str_2):
#                            product_price.append(val_str)
#                            product_price.append(val_str_2)
#                            new_products_prices.append(product_price)
#                    try:
#                        val_str = float(val_str)
#                        val_str_2 = float(val_str_2)
#                    except:
#                        pass
#                    print'val_str88888=------',val_str
#                    print'val_str_2------------=------',val_str_2
#                    if val_str != val_str_2:
#                        
#                        if not lines.keys()[lin] == 'price_unit':
#                            pmsg += _('%s , Field: %s, CSV: %s, OPEN: %s \n')\
#                                % (tools.ustr(prod_name),
#                                   lines.keys()[lin],
#                                   tools.ustr(dat[data[0].
#                                                  index(lines.keys()[lin])]),
#                                   tools.ustr(val_str_2))
#                        if favalidate:
#                            dat[data[0].index(lines.keys()[lin])] = val_str_2
#                        else:
#                            dat[data[0].index(lines.keys()[
#                                              lin])] = val_str or val_str_2
#            datas.append(dat)
#            print'datas==============',datas
#            print'not_products==============',not_products
#            print'new_products_prices==============',new_products_prices
#            try:
#                print'data2===try==import_data=========',data2
#                print'datas===try==import_data=========',datas
#                print'lines===try==import_data=========',lines
#                test = lines and self.pool.get('sale.order.line').import_data(
#                    cr, uid, data2, datas, 'init', '', context=context) or\
#                    False
#                print'101010101-------',test
#            except Exception, e:
#                print'9999999999999------------',e
#                return False
#            data2 = []
#
#        msg += _('Do not you find reference:')
#        msg += '\n'
#        for p in not_products:
#            msg += '%s \n' % (tools.ustr(p))
#        msg += '\n'
#        msg += _(
#            '''Warning of price difference, CSV VS System in
#               the following products:''')
#        msg += '\n'
#        for p in new_products_prices:
#            p2 = (','.join(map(str, p)))
#            msg += '%s \n' % (p2)
#        msg += '\n'
#        msg += _(
#            '''Warning differences in other fields,
#               CSV VS System in the following products and fields:''')
#        msg += '\n %s ' % (pmsg)
#        msg2 = tools.ustr(pmsg)
#        msg = tools.ustr(msg) + '%s ' % (msg2)
        return True
