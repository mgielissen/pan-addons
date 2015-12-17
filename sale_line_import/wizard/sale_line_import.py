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

import base64

from openerp.osv import osv, fields
import logging
logger = logging.getLogger('izard.import')

class wizard_import(osv.TransientModel):
    _name = 'wizard.import'
    _columns = {
        'name': fields.binary('File'),
    }

    def send_lines(self, cr, uid, ids, context=None):
        csv_datas = self.browse(cr, uid, ids).name
        prod_obj = self.pool.get('product.product')
        prod_catge_obj = self.pool.get('product.category')
        prod_tax_obj = self.pool.get('account.tax')
        mrp_bom_obj = self.pool.get('mrp.bom')
        mrp_bom_line_obj = self.pool.get('mrp.bom.line')
        order_obj = self.pool.get('sale.order')
        order_line_obj = self.pool.get('sale.order.line')
        bom_data = base64.decodestring(csv_datas)
        lis = bom_data.splitlines()
        order_id = context.get('active_id', False)
        bom_list = []
        rownum = 0
        for li in lis:
            if rownum==0:
                header = li
                row = li.split(';')
                if row[0] != '':
                    logger.error('row------- %s', row)
                    value1 = str(row[0]).split('(')
                    logger.error('value1------- %s', value1)
                    value = str(value1[1]).strip(' ').split(' ')[0]
                    logger.error('value------- %s', value)
                    catgory = value[:-3]
                    logger.error('catgory------- %s', catgory)
            else:
                logger.error('li---------- %s', li)
                row = li.split(';')
                logger.error('row----tt------ %s', row)
                if len(row)>4:
                    if row[0] in ['COMPOSICIÓN','Cantidad']:
                        continue
                    if row[0] == 'LISTA PRODUCTOS':
                        break
                    if not row[0] == '' and not row[1] == '':
                        logger.error('row---------- %s', row)
                        logger.error('row----len------ %s', len(row))
                        logger.error('row---[0]------- %s', row[4])
                        product_qty1 = str(row[0]).replace(',','.')
                        product_qty = float(product_qty1)
                        product_default_code = str(row[1]).strip(' ')
                        product_dec = str(row[2]).strip(' ')
#                        product_dec = product_dec.encode('utf-8')
                        product_unit_price1 = str(row[5]).replace(',','.')
                        product_unit_price = float(product_unit_price1)
                        child_product_unit_price = row[3]
                        logger.error('child_product_unit_price------- %s', child_product_unit_price)
                        logger.error('product_unit_price------- %s', product_unit_price)
                        if child_product_unit_price == '' and product_unit_price >=0.0:
                            product_default_code = str(value)+'-'+str(product_default_code)
#                            prod_main_id = prod_obj.search(cr,uid,[('default_code','=',product_default_code)])
#                        else:
#                            x
                            
                        logger.error('product_default_code------- %s', product_default_code)
                        logger.error('rownum----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------ %s', rownum)
                        prod_id = prod_obj.search(cr,uid,[('default_code','=',product_default_code)])
                        categ_id = prod_catge_obj.search(cr,uid,[('name','=',catgory)])
                        tax_id = prod_tax_obj.search(cr,uid,[('description','=','IVA 21%')])
#                        if not prod_id:
#                            prod_id = prod_obj.search(cr,uid,[('name','=',product_dec)])
                        
                        if not prod_id:
                            prod_vals = {
                            'name':product_dec,
                            'categ_id':categ_id[0],
                            'taxes_id':[(6, 0, [tax_id[0]])],
                            'default_code':product_default_code,
                            'list_price':product_unit_price,
                            'type':'product',    
                            'sale_ok ':True,    
                            'purchase_ok':False,    
                            }
                            prod_id = prod_obj.create(cr,uid,prod_vals)

                        else:
                            prod_id = prod_id[0]
                            prod_update_vals ={
                            'list_price':product_unit_price
                            }
                            prod_obj.write(cr,uid,prod_id,prod_update_vals)
                            
                        #checking bom  
                        prod_data = prod_obj.browse(cr,uid,prod_id)
                        if child_product_unit_price == '' and product_unit_price >= 0.0:
                            order_line_vals = {
                            'name':product_dec,
                            'product_id':prod_id,
                            'product_uom_qty':product_qty,
                            'tax_id':[(6, 0, [tax_id[0]])],
                            'product_uom':prod_data.uom_id.id,
                            'price_unit':product_unit_price,
                            'order_id':order_id,
                            }
                            order_line_id = order_line_obj.search(cr,uid,[('product_id','=',prod_id),('order_id','=',order_id)])
                            if not len(order_line_id):
                                order_line_obj.create(cr,uid,order_line_vals)
                            else:
                                order_line_data = order_line_obj.browse(cr,uid,order_line_id[0])
                                order_line_vals['product_uom_qty'] = product_qty + order_line_data.product_uom_qty
                                order_line_obj.write(cr,uid,order_line_id[0],order_line_vals)

                            bom_id = mrp_bom_obj.search(cr,uid,[('product_tmpl_id','=',prod_data.product_tmpl_id.id),('type','=','normal')])
                            if not bom_id:
                                bom_vals ={
                                'code':product_dec,
                                'name':prod_data.name,
                                'product_tmpl_id':prod_data.product_tmpl_id.id,
                                'product_id':prod_data.id,
                                'product_uom':prod_data.uom_id.id,
                                'type':'normal',
                                'product_qty':1
                                }
                                bom_id = mrp_bom_obj.create(cr,uid,bom_vals)
                            else:
                                bom_id = bom_id[0]
                                bom_vals ={
                                'code':product_dec,
                                'name':prod_data.name,
                                'product_tmpl_id':prod_data.product_tmpl_id.id,
                                'product_id':prod_data.id,
                                'product_uom':prod_data.uom_id.id,
                                'type':'normal',
                                'product_qty':1
                                }
                                mrp_bom_obj.write(cr,uid,bom_id,bom_vals)
                                all_bom_lines = mrp_bom_line_obj.search(cr,uid,[('bom_id','=',bom_id)])
                                mrp_bom_line_obj.unlink(cr,uid,all_bom_lines,context={})
                            bom_list.append(bom_id)    

                        else:
                            bom_line_vals ={
                                'product_id':prod_id,
                                'product_uom':prod_data.uom_id.id,
                                'product_qty':product_qty,
                                'product_efficiency':1,
                                'type':'normal',
                                'bom_id':bom_id,
                                }

                            mrp_bom_line_obj.create(cr,uid,bom_line_vals)
                            
            rownum+=1
        
        for bom in bom_list:
            all_bom_lines = mrp_bom_line_obj.search(cr,uid,[('bom_id','=',bom)])
            if not len(all_bom_lines):
                mrp_bom_obj.unlink(cr,uid,[bom],context={})
            else:
                bom_info = mrp_bom_obj.browse(cr,uid,bom)
                bom_name_list=[]
                for line in bom_info.bom_line_ids:
                    name = line.product_id.name
                    default_code = line.product_id.default_code
                    if not default_code:
                        default_code =''
                    qty = line.product_qty
                    dec_name = str(default_code.encode('utf-8'))+' '+str(name.encode('utf-8'))+'X'+str(qty)
                    bom_name_list.append(dec_name)
                description_sale = '\n'.join(bom_name_list)
                logger.error('description_sale------- %s', description_sale)
                p_id = bom_info.product_id.id
                prod_obj.write(cr,uid,p_id,{'description_sale':description_sale})
        
        for order in order_obj.browse(cr,uid,[order_id]):
            for line in order.order_line:
                dec = line.product_id.description_sale
                if dec:
                    line.write({'name':dec})
        return True
#    
#    def send_lines(self, cr, uid, ids, context=None):
#        if context is None:
#            context = {}
#        form = self.read(cr, uid, ids, [])
#        order_id = context.get('active_id', False)
#        print'order_id--------',order_id
#        print'from--------',form[0]['name']
#        fdata = form and base64.decodestring(form[0]['name']) or False
#        fvalidate = form and form[0]['validate'] or False
#        print'fvalidate--------',fvalidate
#        print'fdata--------',fdata
#        msg = self.pool.get('sale.order').import_data_line(
#            cr, uid, order_id, fdata, fvalidate, context=context)
#        return True
