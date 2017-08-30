#!/usr/bin/env python
# -*- coding: utf-8 -*-

def ordermodel2dict(order):
	return {
		'id':order.id,
		'order_no':order.order_no,
		'customer_name':order.customer_name,
		'status':order.status,
		'amount':order.amount,
		'tax':order.tax,
		'tip':order.tip,
		'shipping_fee':order.shipping_fee,
		'total_amount':order.total_amount,
		'city':order.city,
		'post_code':order.post_code,
		'state':order.state,
		'state_code':order.state_code,
		'country':order.country,
		'distance':order.distance,
		'create_date':order.create_date,
		'last_update_date':order.last_update_date,
		'add_date':order.add_date
	}

class OrdersModel:

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
	def customer_name(self):
		return self.customer_name
	@customer_name.setter
	def customer_name(self,value):
		self.customer_name=value
		
	@property
	def status(self):
		return self.status
	@status.setter
	def status(self,value):
		self.status=value
		
	@property
	def amount(self):
		return self.amount
	@amount.setter
	def amount(self,value):
		self.amount=value
		
	@property
	def tax(self):
		return self.tax
	@tax.setter
	def tax(self,value):
		self.tax=value
	
	@property
	def tip(self):
		return self.tip
	@tip.setter
	def tip(self,value):
		self.tip=value
			
	@property
	def shipping_fee(self):
		return self.shipping_fee
	@shipping_fee.setter
	def shipping_fee(self,value):
		self.shipping_fee=value
			
	@property
	def total_amount(self):
		return self.total_amount
	@total_amount.setter
	def total_amount(self,value):
		self.total_amount=value
	
	@property
	def city(self):
		return self.city
	@city.setter
	def city(self,value):
		self.city=value
		
	@property
	def post_code(self):
		return self.post_code
	@post_code.setter
	def post_code(self,value):
		self.post_code=value
	
	@property
	def state(self):
		return self.state
	@state.setter
	def state(self,value):
		self.state=value
		
	@property
	def state_code(self):
		return self.state_code
	@state_code.setter
	def state_code(self,value):
		self.state_code=value
		
	@property
	def country(self):
		return self.country
	@country.setter
	def country(self,value):
		self.country=value

	@property
	def distance(self):
		return self.distance
	@distance.setter
	def distance(self,value):
		self.distance=value
		
	@property
	def create_date(self):
		return self.create_date
	@create_date.setter
	def create_date(self,value):
		self.create_date=value
			
	@property
	def last_update_date(self):
		return self.last_update_date
	@last_update_date.setter
	def last_update_date(self,value):
		self.last_update_date=value
		
	@property
	def add_date(self):
		return self.add_date
	@add_date.setter
	def add_date(self,value):
		self.add_date=value
		