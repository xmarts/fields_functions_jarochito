# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import re

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

class AddCampProductProduct(models.Model):

	_inherit = 'product.product'

	units_prod_product = fields.Char( string = 'Cantidad por producto' , compute = '_get_units_prod', readonly = False )

	def _get_units_prod(self):
		units = re.split('/', self.name)
		if len(units) == 2:
			self.units_prod_product = units[1]
		else:
			self.units_prod_product = 0

class AddCampsProductPage(models.Model):

	_inherit = 'product.template'

	units_prod = fields.Char( string = 'Cantidad por producto' , compute = '_get_units', readonly = False )

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

	def _get_units(self):
		units = re.split('/', self.name)
		if len(units) == 2:
			self.units_prod = units[1]
		else:
			self.units_prod = 0

class AddRateAddressDelivery(models.Model):

	_inherit = 'res.partner'

	rate_address = fields.Many2one( 'product.pricelist', string = 'Tarifa' )

	most_ieps = fields.Boolean( string = 'Mostrar IEPS' )

	number_sucursal = fields.Char( string="Numero" )

	type_suc = fields.Selection( [('A','Cedis'),('S','Sucursal'),('O','Oficinas')] , string = 'Tipo')

	format_suc = fields.Char( compute = "getValue", readonly=True )

	gln = fields.Char( string = 'GLN' )

	number_provideer = fields.Char( string = 'Numero de proveedor' )

	def getValue(self):
		if self.number_sucursal and self.type_suc:
			self.format_suc = str(self.type_suc) + str(self.number_sucursal)
		else:
			self.format_suc = ''

class OnchangeDirectionFacture(models.Model):

	_inherit = 'sale.order'

	number_order = fields.Char( string = "Numero de orden" )

	number_appoi = fields.Char( string = "Numero de cita" )

	date_of_deli = fields.Datetime( string = "Fecha de entrega", required = True )

	folio_note_entry = fields.Char( string = "Folio de nota de entrada" )

	field_add_capture = fields.Char( string = "Campo addicional para capturar" )

	@api.onchange('partner_shipping_id')
	def changeDirFac(self):
		if self.partner_shipping_id:
			if self.partner_shipping_id.rate_address.id:
				self.pricelist_id = self.partner_shipping_id.rate_address.id
			else:
				self.pricelist_id = self.partner_shipping_id.property_product_pricelist.id

class AddFIeldManySales(models.Model):

	_inherit = 'account.invoice'

	fields_sales = fields.Many2one( 'sale.order', string = "Campo ventas", compute = "getValue", readonly = True )

	def getValue(self):
		search = self.env['sale.order'].search([('name','=',self.origin)], limit = 1)
		self.fields_sales = search.id

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






