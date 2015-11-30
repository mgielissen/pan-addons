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
from openerp.osv import osv, fields
from datetime import datetime
import datetime
import logging
logger = logging.getLogger('project_code')

class crm_lead(osv.osv):
    _inherit = "crm.lead"
    
    _columns = {
        'projects_id':fields.many2one('project.project', 'Project'),
    }
crm_lead()


class project_task(osv.osv):
    _inherit = "project.task"

    def _get_total_days (self, cr, uid, ids, name, arg, context=None):
        res ={}
        for task_data in self.browse(cr, uid,ids):
            if task_data.date_start:
                if not task_data.project_id.state in ['colose' ,'cancelled']:
                    current = datetime.datetime.now()
                    date_format = "%Y-%m-%d"
                    today = datetime.datetime.strptime(str(current)[:10], date_format)
                    start_date = datetime.datetime.strptime(str(task_data.date_start)[:10], date_format)
                    logger.error('result ------- today ==== %s', today)
                    logger.error('result ------- start_date ==== %s', start_date)
                    difference = today - start_date
                    day = difference.days
                    logger.error('result ------- days ==== %s', day)
                    res[task_data.id]=day
        logger.error('result ------- res ==== %s', res)
        print'res-------',res   
        return res

    def _get_default_date_deadline(self, cr, uid, context=None):
        timeNow = datetime.datetime.now()
        anotherTime = timeNow + datetime.timedelta(days=8)
        
        return anotherTime

    _columns = {
       'latest_task_modified':fields.datetime('Last Task Modified',readonly=True),
       'total_days': fields.function(_get_total_days,
                                         type='integer',
                                         string='Total Days'),
       'date_deadline': fields.date('Deadline', select=True, copy=False),
    }

    _defaults = {
       'date_deadline': _get_default_date_deadline,  
                 
    }

    def write(self, cr, uid, ids ,vals, context=None):
        logger.error('result ------- vals ==== %s', vals)
        befor_task_data = self.browse(cr,uid,ids)
        stage_obj = self.pool.get('project.task.type')
        befor_stage_id = befor_task_data.stage_id.name
        logger.error('befor_stage_id ------- vals ==== %s', befor_stage_id)
        if vals.get('stage_id',False):
	    task_new_data = stage_obj.browse(cr,uid,vals['stage_id'])
            logger.error('befor_stage_id ------- vals ==== %s', task_new_data.name)
            if task_new_data.name =='Finalizado':
                vals['date_end']=datetime.datetime.now()
           
            else:
                vals['date_end']=False
        vals['latest_task_modified']=datetime.datetime.now()
        result = super(project_task,self).write(cr, uid, ids, vals, context)
        task_data = self.browse(cr,uid,ids)
        after_stage_id = task_data.stage_id
        logger.error('after_stage_id ------- vals ==== %s', after_stage_id)
        if task_data.project_id:
           project_obj = self.pool.get('project.project')
	   project_obj.write(cr,uid,task_data.project_id.id,{'latest_task_modified':datetime.datetime.now()})
        return True
    
project_task()

class project_project(osv.osv):
    _inherit = "project.project"
    def create(self, cr, uid, vals, context=None):
        logger.error('vals -new--createcreate---- vals ==== %s', vals)
        result = super(project_project, self).create(cr, uid, vals, context)
        model_obj = self.pool['project.project']   
        if vals.get('members',False):
            if len(vals['members'][0][2]):
                follower_obj = self.pool.get('mail.followers')                 
                for uid_data in self.pool.get('res.users').browse(cr,uid,vals['members'][0][2]):
                    res_model = 'project.project'
                    res_id = result
                    partner_id = uid_data.partner_id.id
                    follower_id = follower_obj.search(cr,uid,[('res_model','=',res_model),('res_id','=',res_id),('partner_id','=',partner_id)])
                    if not len(follower_id):
                        follower_obj.create(cr,uid,{'res_model':res_model,'res_id':res_id,'partner_id':partner_id})
        return result
    def write(self, cr, uid, ids ,vals, context=None):
        logger.error('vals -new---writewritewrite--- vals ==== %s', vals)
        logger.error('vals -new---writewritewrite---ids ==== %s', ids)
        result = super(project_project,self).write(cr, uid, ids, vals, context)
        model_obj = self.pool['project.project']
        if vals.get('members',False):
            if len(vals['members'][0][2]):
                follower_obj = self.pool.get('mail.followers') 
                for uid_data in self.pool.get('res.users').browse(cr,uid,vals['members'][0][2]):
                    res_model = 'project.project'
                    partner_id = uid_data.partner_id.id
                    follower_id = follower_obj.search(cr,uid,[('res_model','=',res_model),('res_id','=',ids[0]),('partner_id','=',partner_id)])
                    logger.error('vals -new---writewritewrite--- follower_id ==== %s', follower_id)
		    if not len(follower_id):
                        follo = follower_obj.create(cr,uid,{'res_model':res_model,'res_id':ids[0],'partner_id':partner_id})
                        logger.error('vals -new---writewritewrite--- follo ==== %s', follo)
        return True

project_project()

class project(osv.osv):
    _inherit = "project.project"
    
    def name_search(self, cr, uid, name, args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search(cr, uid,
                              [('code', '=like', name + "%")] + args,
                              limit=limit)
            if not ids:
                ids = self.search(cr, uid,
                                  [('name', operator, name)] + args,
                                  limit=limit)
        else:
            ids = self.search(cr, uid, args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res


class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account'

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search(cr, uid, [('code', '=like', name + "%")] + args,
                              limit=limit)
            if not ids:
                ids = self.search(cr, uid, [('name', operator, name)] + args,
                                  limit=limit)
        else:
            ids = self.search(cr, uid, args, context=context, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

    def name_get(self, cr, uid, ids, context=None):
        return self._get_full_name(cr, uid, ids, context=context)

    def _get_full_name(self, cr, uid, ids, name=None, args=None, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res
    
    def _get_total_days(self, cr, uid, ids, name=None, args=None, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res
    
    def _get_total_days (self, cr, uid, ids, name, arg, context=None):
        res ={}
        for project_data in self.browse(cr, uid,ids):
            if project_data.date_start:
                if not project_data.state in ['colose' ,'cancelled']:
                    current = datetime.datetime.now()
                    date_format = "%Y-%m-%d"
                    today = datetime.datetime.strptime(str(current)[:10], date_format)
                    start_date = datetime.datetime.strptime(str(project_data.date_start), date_format)
                    logger.error('result ------- today ==== %s', today)
                    logger.error('result ------- start_date ==== %s', start_date)
                    difference = today - start_date
                    day = difference.days
                    logger.error('result ------- days ==== %s', day)
                    res[project_data.id]=day
        logger.error('result ------- res ==== %s', res)
        print'res-------',res   
        return res
   
    _columns = {
        'latest_task_modified':fields.datetime('Last Task Modified',readonly=True),
        'complete_name': fields.function(_get_full_name,
                                         type='char',
                                         string='Full Name'),
        'total_days': fields.function(_get_total_days,
                                         type='integer',
                                         string='Total Days'),
        'version':fields.selection([('v1','v1'),
                                    ('v2','v2'),
                                    ('v3','v3'),
                                    ('v4','v4'),
                                    ('v5','v5'),
                                    ('v6','v6'),
                                    ('v7','v7'),
                                    ('v8','v8'),
                                    ('v9','v9'),
                                    ('v10','v10'),
                                    ('v11','v11'),
                                    ('v12','v12'),
                                    ('v13','v13'),
                                    ('v14','v14'),
                                    ('v15','v15'),
                                    ('v16','v16'),
                                    ('v17','v17'),
                                    ('v18','v18'),
                                    ('v19','v19'),
                                    ('v20','v20')],'Version'),
    }
