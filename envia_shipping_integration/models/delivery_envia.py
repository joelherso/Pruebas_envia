# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from .envia_request import EnviaRequest

class ProviderEnvia(models.Model):
    _inherit = 'delivery.carrier'

    min_price = fields.Float('Precio Minimo')
    delivery_type = fields.Selection(selection_add=[
        ('estafeta', "Estafeta (ENVIA)"),
        ('scm', "SCM (ENVIA)"),
        ('dhl', "DHL (ENVIA)"),
        ('paquete_express', "Paquete Express (ENVIA)"),
        ('fedex', "FedEx (ENVIA)"),
        ], ondelete={
            'scm': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0}),
            'dhl': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0}),
            'fedex': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0}),
            'estafeta': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0}),
            'paquete_express': lambda recs: recs.write({'delivery_type': 'fixed', 'fixed_price': 0})}
        )

    def send_shipping(self, pickings):
        res = []
        shipping_data = {
            'exact_price': 0,
            'tracking_number': 0,
        }
        return res + [shipping_data]


    def dhl_rate_shipment(self, order):
        print ('*******DHL*******')
        carrier = "dhl"
        res = self._rate_shipment_vals(order,carrier)
        return res

    def scm_rate_shipment(self, order):
        print ('*******SCM*******')
        carrier = "scm"
        res = self._rate_shipment_vals(order,carrier)
        return res

    def fedex_rate_shipment(self, order):
        print ('*******FEDEX*******')
        carrier = "fedex"
        res = self._rate_shipment_vals(order,carrier)
        return res

    def estafeta_rate_shipment(self, order):
        print ('*******ESTAFETA*******')
        carrier = "estafeta"
        res = self._rate_shipment_vals(order,carrier)
        return res

    def paquete_express_rate_shipment(self, order):
        print ('*******PAQUETE EXPRESS*******')
        carrier = "paquete_express"
        res = self._rate_shipment_vals(order,carrier)
        return res

    def _rate_shipment_vals(self, order, carrier):
        action = "quote"
        company = order.company_id
        token = company.envia_token_test if company.envia_environment == 'TEST' else company.envia_token
        #Buscamos el peso total del Pedido
        weight = sum(i.product_id.weight * i.product_uom_qty for i in order.order_line)
        
        #Buscamos las Medidas
        measures = self.env['delivery.measure'].get_measure(weight)

        #Conectamos al Endpoint de ENVIA para obtener precio
        srm = EnviaRequest(company.envia_environment, action)
        times = measures['amount']
        order.envia_box_id = False
        order.envia_box_qty = False
        connect = srm.envia_quote_request(order, token, measures, carrier)
        if connect.get('error_message'):
            order.envia_log += connect.get('error_message')
            return {'success': False,
                    'price': 0.0,
                    'error_message': "Método no Disponible",
                    'warning_message': False}

        elif connect.get('data_envia') and 'data' in connect.get('data_envia'):
            price = int(connect.get('data_envia')['data'][0].get('basePrice'))
            order.envia_log = "\n\n%s\n\n%s"%(str(connect.get('data_envia')['data'][0]),order.envia_log)
            order.envia_box_id = measures['box_id']
            order.envia_box_qty = measures['amount']

            return {'success': True,
                    'price': price * times,
                    'error_message': False,
                    'warning_message': False}
        else:
            return {'success': False,
                    'price': 0.0,
                    'error_message': "Servicio no disponible",
                    'warning_message': False}








# ~ {"origin": {"name": "M\u00e9xico", "company": "Envia", "email": false, "phone": "8180162137", "street": "vasconcelos", "number": "1400", "district": "jardines de mirasierra", "city": "tijuana", "state": "nl", "country": "MX", "postalCode": "", "reference": "", "coordinates": {"latitude": "25.655552", "longitude": "-100.397811"}}, "destination": {"name": "M\u00e9xico", "company": "Envia", "email": "admin@example.com", "phone": "87654321", "street": "sendero 99", "number": "1400", "district": "jardines de mirasierra", "city": "Jalisco", "state": "nl", "country": "MX", "postalCode": "66230", "reference": "", "coordinates": {"latitude": "25.655552", "longitude": "-100.397811"}}, "packages": [{"content": "zapatos", "amount": 1, "type": "box", "weight": 1, "insurance": 0, "declaredValue": 0, "weightUnit": "KG", "lengthUnit": "CM", "dimensions": {"length": 11, "width": 15, "height": 20}}], "shipment": {"carrier": "estafeta", "type": 1}, "settings": {"printFormat": "PDF", "printSize": "STOCK_4X6", "currency": "MXN", "cashOnDelivery": "500.00", "comments": ""}}
