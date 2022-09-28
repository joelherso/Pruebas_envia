# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import requests
import logging
_logger = logging.getLogger(__name__)

class EnviaRequest():

    def __init__(self, environment, request_type):
        if request_type == "quote":
            if environment == 'TEST':
                self.url = "https://api-test.envia.com/ship/rate/"
            else:
                self.url = "https://api.envia.com/ship/rate/"
        else:
            if environment == 'TEST':
                self.url = "https://api-test.envia.com/ship/rate/"
            else:
                self.url = "https://api.envia.com/ship/rate/"

    def envia_quote_request(self, order, token, measures, carrier):
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer %s'%token
        }
        dict_response = {
            'data_envia':'',
            'status_request':'',
            'error_message':''
        }
        ship_origin = self._envia_origin_data(order.company_id)
        ship_destination = self._envia_destination_data(order.partner_id)
        ship_package = self._envia_packages_data(order,measures)
        ship_carrier = self._envia_carrier_data(carrier)
        ship_settings = self._envia_settings_data(order)
        request_vals = {
            "origin": ship_origin,
            "destination": ship_destination,
            "packages": [ship_package],
            "shipment": ship_carrier,
            "settings": ship_settings,
        }

        payload = json.dumps(request_vals)
        _logger.info("Conectando con ENVIA url: %s"%self.url)
        _logger.info("Values: %s"%payload)
        request = requests.post(self.url, headers=headers, data=payload)
        _logger.info("RESPUESTA ENVIA: %s"%request)
        request_data = request.content
        request_status = request.status_code
        error = False
        try:
            request_dict = json.loads(request_data)
        except:
            error = True
            request = {'error': request_data}
            request_dict = {'error': {'error': str(request_data), 'code': 401}}
            pass
        _logger.info("RESPUESTA STATUS: %s"%request_status)
        _logger.info("DATA RESPUESTA ENVIA: %s"%request_data)

        if request_status in ('200',200) and not error:
            dict_response['data_envia'] = request_dict
            dict_response['status_request'] = request_status
            if request_dict.get('meta') and request_dict.get('meta') == 'error':
                dict_response['error_message'] = request_dict.get('error').get('message')
            if request_dict.get('code') and request_dict.get('code') in ('400',400):
                dict_response['error_message'] = request_dict.get('message')
        else:
            msg = request
            if request_dict.get('error'):
                error = request_dict['error']
                if error.get('code'):
                    msg = 'Error Codigo %s: %s' %(error.get('code'),error.get('message'))
            else:
                msg = 'Error Codigo %s: %s' %(request_dict.get('code'),request_dict.get('message'))
            dict_response['error_message'] = msg
        # ~ except IOError:
            # ~ dict_response['error_message'] = 'ENVIA Service provided not available or incorrect'
        return dict_response

    def _envia_origin_data(self, company):
        #----- Datos del Origen -----#
        origin_dict = {
            "name": 'Mexico',#company.country_id.name,
            "company": company.name,
            "email": company.email,
            "phone": company.phone,
            "street": company.street,
            "number": "1400",
            "district": "jardines de mirasierra",
            "city": company.city,
            "state": "nl",
            "country": "MX",
            "postalCode": company.zip,
            "reference": "",
            "coordinates": {"latitude": "25.655552", "longitude": "-100.397811"}
            }
        return origin_dict

    def _envia_destination_data(self, partner):
        #----- Datos del Destino -----#
        destination_dict = {
            "name": 'Mexico',#partner.country_id.name,
            "company": partner.name,
            "email": partner.email,
            "phone": partner.phone,
            "street": partner.street,
            "number": "1400",
            "district": "jardines de mirasierra",
            "city": partner.city,
            "state": "nl",
            "country": "MX",
            "postalCode": partner.zip,
            "reference": "",
            "coordinates": {"latitude": "25.655552", "longitude": "-100.397811"}
            }
        return destination_dict

    def _envia_packages_data(self, order, measures):
        content = []
        if len(order.picking_ids) == 1:
            picking = order.picking_ids
        else:
            picking = order.picking_ids.filtered(lambda x:x.picking_type_code == 'outgoing')
        for line in picking.move_lines:
            content.append(line.description_picking)
        shipping_detail = {
            "content": "zapatos",
            "amount": 1,
            "type": "box",
            "weight": 1,
            "insurance": 0,
            "declaredValue": 0,
            "weightUnit": "KG",
            "lengthUnit": "CM",
            "dimensions": {"length": int(measures['X']),"width": int(measures['Y']), "height": int(measures['Z'])}
        }
        return shipping_detail

    def _envia_carrier_data(self, carrier):
        return {"carrier": carrier, "type": 1}

    def _envia_settings_data(self, carrier):
        settings_detail =  {
            "printFormat": "PDF",
            "printSize": "STOCK_4X6",
            "currency": "MXN",
            "cashOnDelivery": "0.00",
            "comments": ""
        }
        return settings_detail

    def validate_len(self, texto, size=1):
        c = 0
        cadena = ""
        while c < size and c < len(texto):
            cadena += texto[c]
            c += 1
        return cadena


'''
       payload = json.dumps({
          "origin": {
            "name": "Mexico",
            "company": "Envia",
            "email": "mexico@envia.com",
            "phone": "8180162137",
            "street": "vasconcelos",
            "number": "1400",
            "district": "jardines de mirasierra",
            "city": "san pedro garza garcia",
            "state": "nl",
            "country": "MX",
            "postalCode": "66236",
            "reference": "",
            "coordinates": {
              "latitude": "25.655552",
              "longitude": "-100.397811"
            }
          },
          "destination": {
            "name": "Mexico",
            "company": "Envia",
            "email": "mexico@envia.com",
            "phone": "8180100135",
            "street": "belisario dominguez",
            "number": "2470 of 310",
            "district": "obispado",
            "city": "monterrey",
            "state": "nl",
            "country": "MX",
            "postalCode": "64060",
            "reference": "",
            "coordinates": {
              "latitude": "25.672530",
              "longitude": "-100.348120"
            }
          },
          "packages": [
            {
              "content": "zapatos",
              "amount": 1,
              "type": "box",
              "weight": 1,
              "insurance": 0,
              "declaredValue": 0,
              "weightUnit": "KG",
              "lengthUnit": "CM",
              "dimensions": {
                "length": 11,
                "width": 15,
                "height": 20
              }
            }
          ],
          "shipment": {
            "carrier": "dhl",
            "type": 1
          },
          "settings": {
            "printFormat": "PDF",
            "printSize": "STOCK_4X6",
            "currency": "MXN",
            "cashOnDelivery": "500.00",
            "comments": ""
          }
        })'''