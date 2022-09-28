##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcón Hernandez
#    (<http://www.ynext.cl>).
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
    'name': 'Envia shipping integration',
    'version': '15.0.1.0.0',
    'author': 'Ynext SpA',
    'maintainer': 'Ynext SpA',
    'website': 'http://www.ynext.cl',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'summary': 'Envia shipping integration.',
    'depends': ['website_sale','product','delivery','mail'],
    'data': [
         'security/ir.model.access.csv',
         'views/product_template_view.xml',
         'views/product_product_view.xml',
         'views/delivery_envia_view.xml',
         'views/sale_view.xml',
         'views/res_company_view.xml',
         'views/delivery_measure.xml',
         'data/delivery_envia_data.xml',
    ],
    'images': ['static/description/banner.jpg'],
}
