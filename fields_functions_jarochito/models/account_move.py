# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_repr

import base64
import requests

from lxml import etree
from lxml.objectify import fromstring
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

CFDI_XSLT_CADENA = 'l10n_mx_edi/data/3.3/cadenaoriginal.xslt'
CFDI_XSLT_CADENA_TFD = 'l10n_mx_edi/data/xslt/3.3/cadenaoriginal_TFD_1_1.xslt'


class AccountMove(models.Model):
    _inherit = 'account.move'

    # date_invoice = fields.Datetime( string = "Fecha Factura" , default = datetime.today() )
    fields_sales = fields.Many2one( 'sale.order', string = "Campo ventas")
    fecha_entrega = fields.Datetime(string="Fecha Entrega")
    pos_order_id = fields.Many2one( 'pos.order', string = "Orden de POS",readonly = True )
    addenda_folio = fields.Char(string='Folio')

    def getDateFormatedAdd(self, paramDate):
        date_time_obj = datetime.strptime(str(paramDate), '%Y-%m-%d')
        date_return = str(date_time_obj.date())
        return date_return.replace('-', '')

    # @api.one
    def getValue(self):
        # search = self.env['sale.order'].search([('name','=',self.invoice_origin)], limit = 1)
        # if search:
        # 	self.fields_sales = search.id
        # else:
        # 	factura = self.env['account.move'].search([('number','=',self.invoice_origin)], limit = 1)
        # 	searchs = self.env['sale.order'].search([('name','=',factura.origin)], limit = 1)
        # 	self.fields_sales = searchs.id
        # searchp = self.env['pos.order'].search([('name','=',self.invoice_origin)], limit = 1)
        # if searchp:
        self.pos_order_id = False

    def _get_values_addenda(self):
        for rec in self:
            for l in rec.edi_document_ids:
                cfdi_3_3_edi = self.env.ref('l10n_mx_edi.edi_cfdi_3_3')
                if l.edi_format_id == cfdi_3_3_edi:
                    invoice = l.move_id
                    return l.edi_format_id._l10n_mx_edi_get_invoice_cfdi_values(invoice)
