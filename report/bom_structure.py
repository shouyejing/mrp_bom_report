## -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp.report import report_sxw


class bom_structure_with_costprice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_with_costprice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_children': self.get_children,
        })

    def get_children(self, object, level=0):
        result = []

        def _get_rec(object, level):
            for l in object:
                res = {}
                res['pname'] = l.product_id.name
                res['pdes'] = l.product_id.description
                res['pcode'] = l.product_id.default_code
                res['pqty'] = l.product_qty
                res['uname'] = l.product_uom.name
                res['level'] = level
                res['code'] = l.bom_id.code
                res['price'] = l.product_id.product_tmpl_id.standard_price
                res['total'] = l.product_qty * l.product_id.product_tmpl_id.standard_price
                res['seller'] = l.product_id.product_tmpl_id.seller_ids[0].name.name if l.product_id.product_tmpl_id.seller_ids else 'Not Set'
                result.append(res)
                if l.child_line_ids:
                    if level < 6:
                        level += 1
                    _get_rec(l.child_line_ids, level)
                    if level> 0 and level< 6:
                        level -= 1
            return result

        children = _get_rec(object, level)

        return children


class report_mrpbomstructure(osv.AbstractModel):
    _name = 'report.mrp_bom_report.report_mrpbomstructure_with_costprice'
    _inherit = 'report.abstract_report'
    _template = 'mrp_bom_report.report_mrpbomstructure_with_costprice'
    _wrapped_report_class = bom_structure_with_costprice
