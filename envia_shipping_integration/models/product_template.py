# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplateDim(models.Model):
    _inherit = 'product.template'

    weight = fields.Float(digits=(10, 3))
    volume = fields.Float(digits=(10, 6))

    product_width = fields.Float('Width (cm)')
    product_length = fields.Float('Length (cm)')
    product_thickness = fields.Float('Thickness (cm)')

    box_width = fields.Float('Box Width (cm)')
    box_length = fields.Float('Box Length (cm)')
    box_thickness = fields.Float('Box Thickness (cm)')
    box_weight = fields.Float(digits=(10, 3))
    box_volume = fields.Float(digits=(10, 6))

    product_by_box = fields.Float('Products by Box', default=1)
    total_weight = fields.Float('Total Weight', compute='_compute_total_weight')

    envia_price = fields.Float('Envia price')

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
    def _compute_total_weight(self):
        """ Calculates Total Weight """
        for product in self:
            product.total_weight = product.product_by_box * product.weight + product.box_weight