# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    envia_token = fields.Char(string='Envia token', groups="base.group_system")
    envia_token_test = fields.Char(string='Envia test token', groups="base.group_system")
    envia_price = fields.Float('Envia price')
    envia_process = fields.Selection([
        ('0', 'Inactivo'),
        ('1', 'Activo')
    ], default='0')
    envia_environment = fields.Selection([
        ('TEST', 'Test'),
        ('PRO', 'Prodution')
    ], default='TEST')

    