# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 ZestyBeanz Technologies Pvt. Ltd.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields

class product_data_correction_list(osv.osv_memory):
    _name = 'product.data.correction.list'
    _columns= {
               'name': fields.char('Name', size=128),
               'select': fields.boolean('Select'),
               'amount': fields.float('Amount'),
               'product_id':  fields.many2one('product.data.correction','Product')
               }
product_data_correction_list()


class product_data_correction(osv.osv_memory):
    _name = 'product.data.correction'
    _columns= {
               'product_list': fields.one2many('product.data.correction.list', 'product_id', 'Product List'),
               }

    def create(self, cr, uid, vals, context=None):
        print vals,' vals'
        return super(product_data_correction, self).create(cr, uid, vals, context=context)

    def delete_duplicates(self,cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            unlink_ids = self.pool.get('product.data.correction.list').search(cr, uid, [('product_id','=',obj.id),('select','=',True)])
            if len(unlink_ids)<1:
                raise osv.except_osv(('Alert!'), ('Select Atleast one record to delete.'))
            self.pool.get('product.data.correction.list').unlink(cr, uid, unlink_ids)
        return osv.except_osv(('Success!'), ('Duplicate records are deleted successfully!'))
        
    def find_duplicates(self,cr, uid, ids, context=None):
        product_list = self.pool.get('product.product').search(cr, uid, [])
        res_list = []
        for obj in self.browse(cr, uid, ids, context=context):
            unlink_ids = self.pool.get('product.data.correction.list').search(cr, uid, [('product_id','=',obj.id)])
            self.pool.get('product.data.correction.list').unlink(cr, uid, unlink_ids)
            for p in self.pool.get('product.product').browse(cr, uid, product_list, context=context):
                res_dict = {}
                res_dict['select'] = False
                res_dict['name'] = p.name
                res_dict['amount'] = p.list_price
                res_dict['product_id'] = obj.id
                res_list.append([0, False, res_dict])
                
            self.write(cr, uid, [obj.id], {'product_list':res_list})
        print res_list,' res_list'
        return True#{'value': {'product_list':res_list}}
product_data_correction()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
