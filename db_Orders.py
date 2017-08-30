#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_Orders
import json

def data_2_model(data):
	model=model_Orders.OrdersModel()
	model.id=data[0]
	model.order_no=data[1]
	model.customer_name=data[2]
	model.status=data[3]
	model.amount=data[4]
	model.tax=data[5]
	model.tip=data[6]
	model.shipping_fee=data[7]
	model.total_amount=data[8]
	model.city=data[9]
	model.post_code=data[10]
	model.state=data[11]
	model.state_code=data[12]
	model.country=data[13]
	model.distance=data[14]
	model.create_date=data[15]
	model.last_update_date=data[16]
	model.add_date=data[17]
	return model

def add(model):
	if len(get(model.order_no,))<=0:
		sql="INSERT INTO `ChengduJaste`.`Orders`(`id`,`order_no`,`customer_name`,`status`,`amount`,`tax`,`tip`,`shipping_fee`,`total_amount`,`city`,`post_code`,`state`,`state_code`,`country`,`distance`,`create_date`,`last_update_date`,`add_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
		paras=(model.id,model.order_no,model.customer_name,model.status,model.amount,model.tax,model.tip,model.shipping_fee,model.total_amount,model.city,model.post_code,model.state,model.state_code,model.country,model.distance,model.create_date,model.last_update_date,model.add_date)
		return True if db.excute_no_query(sql,paras)>0 else False
	else:
		return True

def get(order_no):
	sql="select *from `ChengduJaste`.`Orders` where order_no=%s"
	paras=(order_no,)
	data=db.select(sql,paras)
	return data
