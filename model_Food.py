#!/usr/bin/env python
# -*- coding: utf-8 -*-

def foodmodel2dict(food):
	return {
		'id':food.id,
		'name':food.name,
		'ename':food.ename,
		'model':food.model,
		'price':food.price,
		'category':food.category,
		'enable':food.enable,
		'adddate':food.adddate,
		'last_update_date':food.last_update_date
	}

class FoodModel:

	@property
	def id(self):
		return self.id
	@id.setter
	def id(self,value):
		self.id=value
	
	@property
	def name(self):
		return self.name
	@name.setter
	def name(self,value):
		self.name=value
		
	@property
	def ename(self):
		return self.ename
	@ename.setter
	def ename(self,value):
		self.ename=value
		
	@property
	def model(self):
		return self.model
	@model.setter
	def model(self,value):
		self.model=value
		
	@property
	def price(self):
		return self.price
	@price.setter
	def price(self,value):
		self.price=value
	@property
	def category(self):
		return self.category
	@category.setter
	def category(self,value):
		self.category=value
		
	@property
	def enable(self):
		return self.enable
	@enable.setter
	def enable(self,value):
		self.enable=value
		
	@property
	def adddate(self):
		return self.adddate
	@adddate.setter
	def adddate(self,value):
		self.adddate=value
		
	@property
	def last_update_date(self):
		return self.last_update_date
	@last_update_date.setter
	def last_update_date(self,value):
		self.last_update_date=value
