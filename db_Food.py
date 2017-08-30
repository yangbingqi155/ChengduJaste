#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import model_Food
import json

def data_2_model(data):
	model=model_Food.FoodModel()
	model.id=data[0]
	model.name=data[1]
	model.ename=data[2]
	model.model=data[3]
	model.price=data[4]
	model.category=data[5]
	model.enable=data[6]
	model.adddate=data[7]
	model.last_update_date=data[8]
	return model

def add(model):
	sql="INSERT INTO `ChengduJaste`.`Food`(`id`,`name`,`ename`,`model`,`price`,`category`,`enable`,`adddate`,`last_update_date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
	paras=(model.id,model.name,model.ename,model.model,model.price,model.category,model.enable,model.adddate,model.last_update_date)
	return True if db.excute_no_query(sql,paras)>0 else False

