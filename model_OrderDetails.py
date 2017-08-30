#!/usr/bin/env python
# -*- coding: utf-8 -*-

def orderdetailsmodel2dict(orderdetail):
	return {
		'id':orderdetail.id,
		'order_no':orderdetail.order_no,
		'food_name':orderdetail.food_name,
		'food_model':orderdetail.food_model,
		'quantity':orderdetail.quantity,
		'price':orderdetail.price,
		'price_with_tax':orderdetail.price_with_tax,
		'total_price':orderdetail.total_price,
		'add_date':orderdetail.add_date
	}

class OrderDetailsModel:

	@property
	def id(self):
		return self.id
	@id.setter
	def id(self,value):
		self.id=value
	
	@property
	def order_no(self):
		return self.order_no
	@order_no.setter
	def order_no(self,value):
		self.order_no=value
		
	@property
	def food_name(self):
		return self.food_name
	@food_name.setter
	def food_name(self,value):
		self.food_name=value
		
	@property
	def food_model(self):
		return self.food_model
	@food_model.setter
	def food_model(self,value):
		self.food_model=value
		
	@property
	def quantity(self):
		return self.quantity
	@quantity.setter
	def quantity(self,value):
		self.quantity=value
		
	@property
	def price(self):
		return self.price
	@price.setter
	def price(self,value):
		self.price=value
	
	@property
	def price_with_tax(self):
		return self.price_with_tax
	@price_with_tax.setter
	def price_with_tax(self,value):
		self.price_with_tax=value
			
	@property
	def total_price(self):
		return self.total_price
	@total_price.setter
	def total_price(self,value):
		self.total_price=value
			
	@property
	def add_date(self):
		return self.add_date
	@add_date.setter
	def add_date(self,value):
		self.add_date=value
	