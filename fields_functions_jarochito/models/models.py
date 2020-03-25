# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import re
import datetime

class AddClaseProduct(models.Model):

	_name = 'class.product'

	clase = fields.Char( string = 'Clase' )

	_rec_name = 'clase'

class AddPresentationProduct(models.Model):

	_name = 'presentation.product'

	presentation = fields.Char( string = 'Presentación' )

	_rec_name = 'presentation'

class AddCodeTypeContainerProduct(models.Model):

	_name = 'typecontainer.product'

	code = fields.Char( string = 'Cod. Tipo de envase' )
	
	_rec_name = 'code'

class AddTasteProduct(models.Model):

	_name = 'taste.product'

	taste = fields.Char( string = 'Sabor' )

	_rec_name = 'taste'

class AddCodeBrandProduct(models.Model):

	_name = 'brand.product'

	brand = fields.Char( string = 'Código de marca' )

	_rec_name = 'brand'

class AddFieldUnitsProduct(models.Model):

	_inherit = 'product.product'

	product_units = fields.Char( string = 'Cantidad por producto')

class AddCampsProductPage(models.Model):

	_inherit = 'product.template'


	#-- Relación para agregar clases al producto
	clase_prod = fields.Many2one( 'class.product' , string = 'Clase' )
	
	#-- Relación para agregar una presentación al producto
	presentation_prod = fields.Many2one( 'presentation.product' , string = 'Presentación' )

	#-- Relación para gregar un código al envase del producto 
	code_container_prod = fields.Many2one( 'typecontainer.product' , string = 'Cod. Tipo de envase' )

	# -- Relación para agregar un sabor al producto 
	taste_product = fields.Many2one( 'taste.product' , string = 'Sabor' )

	# -- Relación para gregar un código a la marca del producto
	brand_product = fields.Many2one( 'brand.product' , string = 'Código de marca' )

class AddRateAddressDelivery(models.Model):

	_inherit = 'res.partner'

	rate_address = fields.Many2one( 'product.pricelist', string = 'Tarifa' )

	most_ieps = fields.Boolean( string = 'Mostrar IEPS' )

	number_sucursal = fields.Char( string="Numero" )

	type_suc = fields.Selection( [('A','Cedis'),('S','Sucursal'),('O','Oficinas')] , string = 'Tipo')

	type_customer = fields.Selection([('mayorista','Mayorista'),('maquila','Maquila'),('autoservicios','Autoservicios'),('rutas','Rutas')], string = 'Tipo de cliente')

	format_suc = fields.Char( compute = "getValue", readonly=True )

	gln = fields.Char( string = 'GLN' )

	number_provideer = fields.Char( string = 'Numero de proveedor' )

	shipping_number_provider = fields.Char( string = "Numero de proveedor" )

	shipping_number_store = fields.Char( string = "Numero de tienda" )

	shipping_number_cedis = fields.Char( string = "Numero de cedis" )

	shipping_type_suc = fields.Selection( [('A','Cedis'),('S','Sucursal'),('O','Oficinas')] , string = 'Tipo')

	shipping_gln = fields.Char( string = "GLN" )

	contact_name = fields.Char(string="Nombre de contacto")

	def getValue(self):
		if self.number_sucursal and self.type_suc:
			self.format_suc = str(self.type_suc) + str(self.number_sucursal)
		else:
			self.format_suc = ''

class OnchangeDirectionFacture(models.Model):

	_inherit = 'sale.order'

	addenda_normal = fields.Boolean( string = "Factura normal" , default = False )

	addenda_extemporanea = fields.Boolean( string = "Factura extemporanea" , default = False)

	number_order = fields.Char( string = "Numero de orden" )

	number_appoi = fields.Char( string = "Numero de cita" )

	date_of_order = fields.Date( string = "Fecha del pedido del cliente" )

	date_of_deli = fields.Date( string = "Fecha de entrega", required = True )

	folio_note_entry = fields.Char( string = "Folio de nota de entrada" )

	field_add_capture = fields.Char( string = "Campo addicional para capturar" )

	@api.onchange('addenda_normal')
	def changeAddendaNormal(self):
		if self.addenda_normal == True:
			self.addenda_extemporanea = False
			search = self.env['ir.ui.view'].search([('name','=','SorianaFacturaNormal')], limit = 1)
			if search:
				self.partner_id.write({'l10n_mx_edi_addenda':search.id})
	
	@api.onchange('addenda_extemporanea')
	def changeAddendaExtemporanea(self):
		if self.addenda_extemporanea == True:
			self.addenda_normal = False
			search = self.env['ir.ui.view'].search([('name','=','SorianaFacturaExtemporanea')], limit = 1)
			if search:
				self.partner_id.write({'l10n_mx_edi_addenda':search.id})

	@api.onchange('partner_shipping_id')
	def changeDirFac(self):
		if self.partner_shipping_id:
			if self.partner_shipping_id.rate_address.id:
				self.pricelist_id = self.partner_shipping_id.rate_address.id
			else:
				self.pricelist_id = self.partner_shipping_id.property_product_pricelist.id

class AddFIeldManySales(models.Model):

	_inherit = 'account.invoice'

	#date_invoice = fields.Datetime( string = "Fecha Factura" , default = datetime.today() )

	fields_sales = fields.Many2one( 'sale.order', string = "Campo ventas", compute = "getValue", readonly = True )
	pos_order_id = fields.Many2one( 'pos.order', string = "Orden de POS", compute = "getValue", readonly = True )
	date_of_sale_order = fields.Date(string="Fecha de pedido del cliente")

	def getDateFormatedAdd(self, paramDate):
		date_time_obj = datetime.datetime.strptime(str(paramDate), '%Y-%m-%d')
		date_return = str(date_time_obj.date())
		return date_return.replace('-','')
		
	@api.one
	def getValue(self):
		search = self.env['sale.order'].search([('name','=',self.origin)], limit = 1)
		if search:
			self.fields_sales = search.id
		else:
			factura = self.env['account.invoice'].search([('number','=',self.origin)], limit = 1)
			searchs = self.env['sale.order'].search([('name','=',factura.origin)], limit = 1)
			self.fields_sales = searchs.id
		searchp = self.env['pos.order'].search([('name','=',self.origin)], limit = 1)
		if searchp:
			self.pos_order_id = searchp.id

class AddFieldGLNCompany(models.Model):

	_inherit = 'res.company'

	field_gln_company = fields.Char( string = "GLN empresa" )
	field_num_levicom = fields.Char( string = "Levicom" )
	field_num_certificate = fields.Char( string = "Numero de aprovación del certificado" )

class AddFieldsContacts(models.Model):

	_inherit = 'res.partner'

	number_store = fields.Char( string = "Numero de tienda" )

class LabelsPallets(models.Model):

	_name = 'labels.pallets'

	def _name_default(self):
		cr = self.env.cr
		cr.execute('select "id" from "labels_pallets" order by "id" desc limit 1')
		id_returned = cr.fetchone()
		if id_returned == None:
			id_returned = (0,)
		text = ''
		pref = 'Etiq-'
		if((max(id_returned) + 1) < 100):
			text = pref + '00' + str(max(id_returned) + 1)
		else:
			text = pref + str(max(id_returned) + 1)
		return text

	name = fields.Char( string = "Nombre", readonly = True, default = _name_default )

	turn = fields.Selection( [('mat','Matutino'),('ves','Vespertino'),('noc','Nocturno')], string = "Turno" )

	pallet = fields.Many2one( 'pallets', string = "Tarima" )

	date = fields.Date( string = "Fecha" )

class Pallets(models.Model):

	_name = 'pallets'

	pallet_name = fields.Char( string = "Tarima" )

	_rec_name = 'pallet_name'


class AddAccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    number_days = fields.Integer(
        string='Numero de dias',
    )

class AddFieldsBank(models.Model):
	"""docstring for Add"""
	_inherit = "res.partner.bank"

	last_acc_number = fields.Char(string="ultimos 4 digitos")

	
	def get_last_numbers(self):
		if self.acc_number:
			self.last_acc_number = self.acc_number[-4:]
			