from odoo import models, fields, api, _


class DeliveryMeasure(models.Model):
    _name = "delivery.measure"
    _description = 'Medidas de Envio'

    name = fields.Char('Tipo Caja')
    uom_id = fields.Many2one('uom.uom', 'Unidad',required=True)
    price = fields.Monetary('Precio', index=True)
    weight_beg = fields.Float('Peso Desde', required=True)
    weight_end = fields.Float('Peso Hasta', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    package_type = fields.Selection([
        ('box', 'CAJA'),
        ('pallet', 'PALETA'),
        ('envelope', 'SOBRE')],
        default='box', string='Tipo',required=True)
    height = fields.Float('Alto')
    length = fields.Float('Largo')
    width = fields.Float('Ancho')
    product_id = fields.Many2one('product.product', required=True, string='Producto')

    def get_measure(self,weight):
        record = self.search([('weight_beg','<=',weight),('weight_end','>=',weight)],limit=1)
        if record:
            var_x = var_y = var_z = 0
            amount = 1
            if record:
                var_x = record.length
                var_y = record.width
                var_z = record.height
            return {'X': var_x,'Y': var_y, 'Z': var_z, 'amount': amount, 'box_id': record.id}
        return self.best_box_ever(weight)

    def best_box_ever(self, weight):
        boxes = self.search([('weight_end','!=',0)], order='weight_end asc')
        last_int = 0
        last_float = 0
        best_box = False
        var_x = var_y = var_z = 0
        for box in boxes:
            divided = str(weight / box.weight_end).split('.')
            int_qty = int(divided[0])
            float_qty = float(str('0.%s')%divided[1])
            if float_qty == 0:
                last_int = int_qty
                best_box = box
                break
            elif float_qty > last_float:
                last_float = float_qty
                last_int = int_qty
                best_box = box
            elif float_qty <= last_float:
                break
        if best_box:
            if last_float != 0:
                last_int += 1
            var_x = best_box.length
            var_y = best_box.width
            var_z = best_box.height
            best_box = best_box.id
        return {'X': var_x, 'Y': var_y, 'Z': var_z, 'amount': last_int, 'box_id': best_box}


