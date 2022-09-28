# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProductDim(models.Model):
    _inherit = 'product.product'

    weight = fields.Float(digits=(10, 3))
    volume = fields.Float(digits=(10, 6))

    total_weight = fields.Float('Total Weight', compute='_compute_total_weight_v')

    @api.onchange('product_width', 'product_length', 'product_thickness')
    def onchange_for_volume(self):
        print("onchange_for_volume")
        """ Calculates Product Volume"""
        for record in self:
            record.volume = record.product_width * record.product_length * record.product_thickness / 1000000.0

    @api.onchange('box_width', 'box_length', 'box_thickness')
    def onchange_for_box_volume(self):
        print("onchange_for_box_volume")
        """ Calculates Box Volume"""
        for record in self:
            record.box_volume = record.box_width * record.box_length * record.box_thickness / 1000000.0

    @api.depends('product_by_box', 'weight', 'box_weight')
    def _compute_total_weight_v(self):
        """ Calculates Total Weight """
        for product in self:
            product.total_weight = product.product_by_box * product.weight + product.box_weight