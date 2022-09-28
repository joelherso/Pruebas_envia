# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    envia_weight = fields.Float('Envia Peso Total', digits=(10, 3), compute='exe_envia')
    envia_shipping_cost = fields.Float('Envia shipping cost')
    envia_log = fields.Text(copy=False)
    envia_box_id = fields.Many2one('delivery.measure', copy=False, string='Caja', readonly=1)
    envia_box_qty = fields.Integer(copy=False, string='Cant. Cajas', readonly=1)

    def _envia_get_weight(self):
        weight = 0
        for record in self:
            for line in record.order_line:
                weight += line.product_id.total_weight * line.product_uom_qty
        return weight

    @api.depends('order_line','order_line.product_id')
    def exe_envia(self):
        for record in self:
            record.envia_weight = self._envia_get_weight()
    """ 
    def _create_delivery_line(self,carrier, amount):
        res = super()._create_delivery_line(carrier, amount)
        self._on_save_box_write_its_product()
        return res """

    def _on_save_box_write_its_product(self):
        for order in self:
            if order.envia_box_id:
                box_line = order.order_line.filtered_domain([('envia_box_id','!=',False)])
                vals = {
                    'product_id': order.envia_box_id.product_id.id,
                    'name': order.envia_box_id.product_id.name,
                    'product_uom_qty': order.envia_box_qty,
                    'price_unit': order.envia_box_id.price,
                    'envia_box_id': order.envia_box_id.id,
                }
                if box_line:
                    box_line.write(vals)
                else:
                    vals.update({
                        'order_id': order.id,
                        'envia_box_id': order.envia_box_id.id,
                    })
                    self.order_line.create(vals)
            else:
                order.order_line.filtered_domain([('envia_box_id','!=',False)]).unlink()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    envia_box_id = fields.Many2one('delivery.measure', copy=False, string='Caja', readonly=1)