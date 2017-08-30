#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_OrderDetails
import json

def data_2_model(data):
	model=model_OrderDetails.OrderDetailsModel()
	model.id=data[0]
	model.order_no=data[1]
	model.food_name=data[2]
	model.food_model=data[3]
	model.quantity=data[4]
	model.price=data[5]
	model.price_with_tax=data[6]
	model.total_price=data[7]
	model.add_date=data[8]
	return model

def add(model):
	sql="INSERT INTO `ChengduJaste`.`OrderDetails`(`id`,`order_no`,`food_name`,`food_model`,`quantity`,`price`,`price_with_tax`,`total_price`,`add_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
	paras=(model.id,model.order_no,model.food_name,model.food_model,model.quantity,model.price,model.price_with_tax,model.total_price,model.add_date)
	return True if db.excute_no_query(sql,paras)>0 else False

