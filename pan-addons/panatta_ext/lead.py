# -*- coding: utf-8 -*-
##############################################################################
#
#    TeckZilla Software Solutions and Services
#    Copyright (C) 2012-2013 TeckZilla-OpenERP Experts(<http://www.teckzilla.net>).
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

from openerp.osv import osv, fields
import logging
logger = logging.getLogger('lead')

class crm_lead(osv.osv):
    _inherit = "crm.lead"
    
    def create(self, cr, uid, vals, context=None):
        result = super(crm_lead, self).create(cr, uid, vals, context)
        cr.commit()
        logger.error('result --- crm_lead---- result ==== %s', result)
        sector =''
        tags = []
        data_opportunity = self.browse(cr, uid, result)
        ir_mail_server = self.pool.get('ir.mail_server')
        mail_mail = self.pool.get('mail.mail')
        all_outemail_ids = ir_mail_server.search(cr,uid,[])
        logger.error('all_outemail_ids --- crm_lead----  ==== %s', all_outemail_ids)
        if data_opportunity.user_id.login:
            if len(data_opportunity.categ_ids):
                for tag in data_opportunity.categ_ids:
                    tags.append(tag.name)
                sector= str(', '.join(tags).encode('utf-8'))
            all_outemail_data = ir_mail_server.browse(cr,uid,all_outemail_ids[0])

            description = ''
            if data_opportunity.description:
                description = str(data_opportunity.description.encode('utf-8'))

            city = ''
            if data_opportunity.city:
                city = str(data_opportunity.city.encode('utf-8'))

            source_id = ''
            if data_opportunity.source_id:
                source_id = str(data_opportunity.source_id.name.encode('utf-8'))

            state = ''
            if data_opportunity.state_id.name:
                state = (data_opportunity.state_id.name.encode('utf-8'))

            phone = ''
            if data_opportunity.phone:
                phone = str(data_opportunity.phone.encode('utf-8'))
                
            saleperson = str(data_opportunity.user_id.name.encode('utf-8'))
            login = data_opportunity.user_id.login.encode('utf-8')
            opportunity_name = str(data_opportunity.name.encode('utf-8'))

            url = 'http://54.77.254.169:8069/web?db=panatta_db#id='+str(data_opportunity.id)+'&view_type=form&model=crm.lead&menu_id=138&action=145'
            create_date = str(data_opportunity.create_date).split(' ')[0]
            values={
                'subject':source_id+'-'+opportunity_name,
                'body_html':'<br/>Content: <br/>'+saleperson+'<br/><br/></n>Nombre: '+opportunity_name+'<br/>Origen: '+source_id+'<br/>Sector: '+sector+'<br/>Localidad: '+city+'<br/>Provincia: '+state+'<br/>Creado: '+create_date+'<br/>Telefono: '+phone+'<br/><br/><br/></n>Descripcion:<br/>'+description+'<br/><br/><br/></n>Puedes ver este Cliente Potencial en:<br/>'+url,
                'email_from':all_outemail_data.smtp_user,
                'email_to':login,
            }

            msg_id = mail_mail.create(cr, uid, values)
            cr.commit()
            mail_mail.send(cr, uid, [msg_id], auto_commit=True, context=context)
        return result
#        
    def write(self, cr, uid, ids ,vals, context=None):
        user_id_before = False
        user_id_bef = self.browse(cr,uid,ids[0])
        if user_id_bef.user_id:
            user_id_before = user_id_bef.user_id.id
        result = super(crm_lead,self).write(cr, uid, ids, vals, context)
        cr.commit()
        user_id_aft = self.browse(cr,uid,ids[0])
        user_id_after = False
        if user_id_aft.user_id:
            user_id_after = user_id_aft.user_id.id
        logger.error('user_id_after --- crm_lead----  ==== %s', user_id_after)    
        logger.error('user_id_before --- crm_lead----  ==== %s', user_id_before)    
        if  user_id_after and user_id_before:
            if user_id_before != user_id_after:
    #            logger.error('result --- crm_lead---- result ==== %s', result)
                sector =''
                tags = []
                data_opportunity = user_id_after
                ir_mail_server = self.pool.get('ir.mail_server')
                mail_mail = self.pool.get('mail.mail')
                all_outemail_ids = ir_mail_server.search(cr,uid,[])
                if data_opportunity.user_id.login:
                    if len(data_opportunity.categ_ids):
                        for tag in data_opportunity.categ_ids:
                            tags.append(tag.name)
                        sector= str(', '.join(tags).encode('utf-8'))
                    all_outemail_data = ir_mail_server.browse(cr,uid,all_outemail_ids[0])

                    description = ''
                    if data_opportunity.description:
                        description = str(data_opportunity.description.encode('utf-8'))

                    city = ''
                    if data_opportunity.city:
                        city = str(data_opportunity.city.encode('utf-8'))

                    source_id = ''
                    if data_opportunity.source_id:
                        source_id = str(data_opportunity.source_id.name.encode('utf-8'))

                    state = ''
                    if data_opportunity.state_id.name:
                        state = (data_opportunity.state_id.name.encode('utf-8'))

                    phone = ''
                    if data_opportunity.phone:
                        phone = str(data_opportunity.phone.encode('utf-8'))

                    saleperson = str(data_opportunity.user_id.name.encode('utf-8'))
                    login = data_opportunity.user_id.login.encode('utf-8')
                    opportunity_name = str(data_opportunity.name.encode('utf-8'))

                    url = 'http://54.77.254.169:8069/web?db=panatta_db#id='+str(data_opportunity.id)+'&view_type=form&model=crm.lead&menu_id=138&action=145'
                    create_date = str(data_opportunity.create_date).split(' ')[0]
                    values={
                        'subject':source_id+'-'+opportunity_name,
                        'body_html':'<br/>Content: <br/>'+saleperson+'<br/><br/></n>Nombre: '+opportunity_name+'<br/>Origen: '+source_id+'<br/>Sector: '+sector+'<br/>Localidad: '+city+'<br/>Provincia: '+state+'<br/>Creado: '+create_date+'<br/>Telefono: '+phone+'<br/><br/><br/></n>Descripcion:<br/>'+description+'<br/><br/><br/></n>Puedes ver este Cliente Potencial en:<br/>'+url,
                        'email_from':all_outemail_data.smtp_user,
                        'email_to':login,
                    }

                    msg_id = mail_mail.create(cr, uid, values)
                    cr.commit()
                    mail_mail.send(cr, uid, [msg_id], auto_commit=True, context=context)
        return True
        
        
#    def get_tages(self,obj):
##        Sector:  ${object.get_tages(object)}
#        tags = []
#        str = ''
#        if len(obj.categ_ids):
#            for tag in obj.categ_ids:
#                tags.append(tag.name)
#            str = ', '.join(tags)
#        return str
crm_lead()