#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import logging
import io
import codecs
import requests
from lxml import etree
import json
import threading
from datetime import datetime, date
import uuid
import sys
import re
import time
import urlparse
from requests_toolbelt import MultipartEncoder

try:
	import cPickle as pickle
except ImportError:
	import pickle
import config
import basic
import libhttpproxy
import db_IPProxiesPoolApplicationSwitch
import model_IPProxiesPoolApplicationSwitch
import model_Food
import model_Orders
import model_OrderDetails
import db_Orders
import db_OrderDetails
import db_Food

sys.setrecursionlimit(1000000) 
has_p_info_pages=0
p_list_url='https://www.amazon.in/s/ref=s9_acss_bw_cts_VodooFS_T1L4_w?rh=n%3A976419031%2Cn%3A!976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cp_98%3A10440597031&qid=1484135102&bbn=1389432031&low-price=&high-price=5%2C000&x=6&y=10&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-7&pf_rd_r=N8FAX8586W73XVCYYS7Y&pf_rd_t=101&pf_rd_p=476f8f1a-15ac-4693-b157-8657b9ebf7e1&pf_rd_i=1389401031'

def get_product_info_urls(req,p_list_page_url,cookies={}):
	next_page_url= ''
	status_code=''
	is_break=False
	result=[]
	try:
		r=basic.get_html_with_session(req,p_list_page_url,cookies=cookies)
		html=r.text
		status_code=r.status_code
		content=etree.HTML(html)
		result=content.xpath("//table[@class='list']/tbody/tr/td/a")

		next_page_elements=content.xpath("//div[@class='pagination']/div[@class='links']/*")
		current_index=0
		for item in next_page_elements:
			if item.tag=='b':
				break
			current_index=current_index+1

		if current_index>=len(next_page_elements)-1:
			next_page_element=None
		else:
			next_page_element=next_page_elements[current_index+1]
		if next_page_element!=None:
			next_page_url=next_page_element.get("href")
			next_page_url=next_page_url
		else:
			#如果最后一页
			print 'The end list page :'+p_list_page_url
			logging.info('The end list page :'+p_list_page_url)
			return [map(lambda x:x.get("href"),result) if result!=None and len(result)>0 else None,'',True]
		
	except  requests.exceptions.Timeout as e:
		print 'request connection timeout error ,product list error url:'+p_list_page_url
		logging.exception('request connection timeout error ,product list error url:'+p_list_page_url)
		return [None,'',False]
	except  requests.exceptions.ConnectionError as e:
		print 'request connection error ,product list error url:'+p_list_page_url
		logging.exception('request connection error ,product list error url:'+p_list_page_url)
		return [None,'',False]
	except  requests.exceptions.RequestException as e:
		print 'request timeout ,product list error url:'+p_list_page_url+',status_code:'+str(status_code)
		logging.exception('request timeout,product list error url:'+p_list_page_url+',status_code:'+str(status_code))
		return [None,'',False]
	except BaseException as e:
		print 'product list error url:'+p_list_page_url+',status_code:'+str(status_code)
		logging.exception('product list error url:'+p_list_page_url+',status_code:'+str(status_code))
		return [None,'',False]
	return [map(lambda x:x.get("href"),result),next_page_url,is_break]

#获取产品详细信息
def get_product_info(req,p_info_url):
	order_info=model_Orders.OrdersModel()
	order_details=[]
	status_code=200
	html=''
	try:
		r=basic.get_html_with_session(req,p_info_url)
		html=r.text
		status_code=r.status_code
		content=etree.HTML(html)
		order_info_rows=content.xpath("//div[@id='tab-order']/table/tr")
		order_details_rows=content.xpath("//div[@id='tab-product']/table/tbody")
		order_shipping_rows=content.xpath("//div[@id='tab-shipping']/table/tr")

		print(p_info_url)
		#Order info
		order_no=order_info_rows[0][1].text.strip().replace("#","")
		customer_name=order_info_rows[2][1].text.strip()
		status=order_info_rows[5][1].text.strip()
		amount=order_details_rows[1][0][1].text.strip().replace("$","")
		tax=order_details_rows[2][0][1].text.strip().replace("$","")
		tip=order_details_rows[4][0][1].text.strip().replace("$","")
		shipping_fee=order_details_rows[3][0][1].text.strip().replace("$","")
		#total_amount=order_details_rows[5][0][1].text.strip().replace("$","")
		city=order_shipping_rows[2][1].text.strip()
		post_code=order_shipping_rows[3][1].text.strip()
		state='' if order_shipping_rows[4][1].text==None else order_shipping_rows[4][1].text.strip()
		state_code='' if len(order_shipping_rows)<=7 else order_shipping_rows[5][1].text.strip()
		country=order_shipping_rows[len(order_shipping_rows)-2][1].text.strip()
		distance=order_shipping_rows[len(order_shipping_rows)-1][1].text.strip()
		create_date=order_info_rows[len(order_info_rows)-2][1].text.strip()
		last_update_date=order_info_rows[len(order_info_rows)-1][1].text.strip()
		add_date=str(datetime.now())
		
		m=re.match('([0-9\.]+)\n\([0-9\.]+\)',shipping_fee)
		if m!=None:
			shipping_fee=m.group(1)

		m_amount=re.match('([0-9\.]+)\n\([0-9\.]+\)',amount)
		if m_amount!=None:
			amount=m_amount.group(1)
			
		total_amount=float(amount)+float(tax)+float(tip)+float(shipping_fee)
		total_amount=round(total_amount,2)
		
		order_info.id=str(uuid.uuid1())
		order_info.order_no=order_no
		order_info.customer_name=customer_name
		order_info.status=status
		order_info.amount=amount
		order_info.tax=tax
		order_info.tip=tip
		order_info.shipping_fee=shipping_fee
		order_info.total_amount=total_amount
		order_info.city=city
		order_info.post_code=post_code
		order_info.state=state
		order_info.state_code=state_code
		order_info.country=country
		order_info.distance=distance
		order_info.create_date=create_date
		order_info.last_update_date=last_update_date
		order_info.add_date=add_date
		
		order_data= json.dumps(order_info,default=model_Orders.ordermodel2dict)
		print(order_data)
		
		#order details
		for index in range(len(order_details_rows[0])):
			item=order_details_rows[0][index]
			food_name=item[0][0].text.strip().encode('utf-8')
			food_model=item[1].text.strip().encode('utf-8')
			quantity=item[2].text.strip()
			price=item[3].text.strip().replace("$","")
			price_with_tax=item[3].text.strip().replace("$","")
			total_price=item[4].text.strip().replace("$","")
			
			m_total_price=re.match('([0-9\.]+) \(([0-9\.]+)\)',total_price)
			if m_total_price!=None:
				total_price=m_total_price.group(1)
				
			m_price=re.match('([0-9\.]+) \(([0-9\.]+)\)',price)
			if m_price!=None:
				price_with_tax=m_price.group(1)
				price=m_price.group(2)
			
			order_detail=model_OrderDetails.OrderDetailsModel()
			order_detail.id=str(uuid.uuid1())
			order_detail.order_no=order_no
			order_detail.add_date=str(datetime.now())
			order_detail.food_name=food_name
			order_detail.food_model=food_model
			order_detail.quantity=quantity
			order_detail.price=price
			order_detail.price_with_tax=price_with_tax
			order_detail.total_price=total_price
			order_details.append(order_detail)
			order_detail_data= json.dumps(order_detail,default=model_OrderDetails.orderdetailsmodel2dict)
			print(order_detail_data)
	
	except  requests.exceptions.Timeout as e:
		print 'request connection timeout error ,product info error url:'+p_info_url
		logging.exception('request connection timeout error ,product info error url:'+p_info_url)
		return None,None
	except  requests.exceptions.ConnectionError as e:
		print 'request connection error ,product info error url:'+p_info_url
		logging.exception('request connection error ,product info error url:'+p_info_url)
		return None,None
	except  requests.exceptions.RequestException as e:
		print 'request timeout ,product info error url:'+p_info_url+',status_code:'+str(status_code)
		logging.exception('request timeout,product info error url:'+p_info_url+',status_code:'+str(status_code))
		return None,None
	except IndexError as e:
		print e
		time.sleep(5)
		return None,None
	except BaseException as e:
		print 'product info error url:'+p_info_url+',status_code:'+str(status_code)
		logging.exception('product info error url:'+p_info_url+',status_code:'+str(status_code))
		#basic.html_write(html,'abc.html')
		#raise e
		return None,None
	return order_info,order_details
#分页扑爬取产品列表页
def go_p_list_page(req,p_list_url,cookies={}):
	next_page_url=''
	p_info_urls=''
	url=p_list_url
	p_data=''
	is_break=False
	p_info_urls,next_page_url,is_break=get_product_info_urls(req,url,cookies=cookies)

	while True:
		#product info page url on the product list page
		p_info_urls,next_page_url,is_break=get_product_info_urls(req,url,cookies)
		#每抓取一页产品列表页切换一次代理
		change_proxy()
		if p_info_urls==None:
			continue
		
		all_thread=[]
		
		for info_url in p_info_urls:
			#add_product(info_url)
			thread=threading.Thread(target=add_product,args=(req,info_url))
			all_thread.append(thread)
			thread.start()
		for thread in all_thread:
			thread.join()
		if 	next_page_url=='':
			logging.info('end of product list page,break:'+url)
			print 'end of product list page,break:'+url
			break
		else:
			url=next_page_url
			logging.info('product list next page:'+url+",p_info_urls length:")
			print 'product list next page:'+url+",p_info_urls length:"
#添加产品到数据库
def add_product(req,info_url):
	if info_url==None or info_url=='':
		return

	while True:
		model,order_details=get_product_info(req,info_url)
		time.sleep(3)
		#每抓取一页产品详细页切换一次代理
		change_proxy()
		if model!=None:
			try:
				order_data= json.dumps(model,default=model_Orders.ordermodel2dict)
				db_Orders.add(model)
				for item in order_details:
					db_OrderDetails.add(item)
			except BaseException as e:
				logging.exception('error order info url:'+info_url)
				logging.exception('error order info data:'+order_data)
				print 'error order info url:'+info_url
				print 'error order info data:'+order_data
				raise e
			logging.info(order_data+"\n")
			print(order_data+"\n")
			break
		else:
			print 'can\'t get order info,order info url:'+info_url
			logging.info('can\'t get order info,order info url:'+info_url)
			continue
			
#添加菜品到数据库
def add_food(foods):
	if foods!=None and len(foods)==0:
		return
	for model in foods:
		time.sleep(3)
		try:
			food_data= json.dumps(model,default=model_Food.foodmodel2dict)
			db_Food.add(model)
			logging.info(food_data+"\n")
			print(food_data+"\n")
		except BaseException as e:
			logging.exception('error add food info data to database:'+food_data)
			print 'error add food info data to database:'+food_data
			raise e
def get_foods(food_url):
	for index in range(1,3):
		url=food_url+"&page="+str(index)
		while True:
			foods=get_food_info(req,url)
			if foods!=None and len(foods)!=0:
				add_food(foods)
				break
			else:
				change_proxy()
	
#获取菜品详细信息
def get_food_info(req,info_url):
	foods=[]
	status_code=200
	html=''
	try:
		r=basic.get_html_with_session(req,info_url)
		html=r.text
		status_code=r.status_code
		content=etree.HTML(html)
		foods_rows=content.xpath("//div[@class='content']/form[@id='form']/table[@class='list']/tbody/tr")
		print(len(foods_rows))
		for index in range(1,len(foods_rows)):
			food_info=model_Food.FoodModel()
		
			#Order info
			name=foods_rows[index][2][1][0].text.strip()
			ename=foods_rows[index][2][2][0].text.strip()
			model=foods_rows[index][7][1].text.strip()
			price=foods_rows[index][8][1].text.strip()
			category=foods_rows[index][4][1][0].text.strip()
			enable_str=foods_rows[index][11][0][0].text.strip()
			enable=True if enable_str==u'停用' else False
			
			food_info.id=str(uuid.uuid1())
			food_info.name=name
			food_info.ename=ename
			food_info.model=model
			food_info.price=price
			food_info.category=category
			food_info.enable=enable
			food_info.adddate=str(datetime.now())
			food_info.last_update_date=str(datetime.now())
		
			food_data= json.dumps(food_info,default=model_Food.foodmodel2dict)
			print(food_data)
			foods.append(food_info)
	
	except  requests.exceptions.Timeout as e:
		print 'request connection timeout error ,food info error url:'+info_url
		logging.exception('request connection timeout error ,food info info error url:'+info_url)
		return None
	except  requests.exceptions.ConnectionError as e:
		print 'request connection error ,food info error url:'+info_url
		logging.exception('request connection error ,food info error url:'+info_url)
		return None
	except  requests.exceptions.RequestException as e:
		print 'request timeout ,food info error url:'+info_url+',status_code:'+str(status_code)
		logging.exception('request timeout,food info error url:'+info_url+',status_code:'+str(status_code))
		return None
	except IndexError as e:
		print e
		time.sleep(5)
		return None
	except BaseException as e:
		print 'food info error url:'+info_url+',status_code:'+str(status_code)
		logging.exception('food info error url:'+info_url+',status_code:'+str(status_code))
		#basic.html_write(html,'abc.html')
		#raise e
		return None
	return foods
	
#启用代理
def set_proxy_enable():
	set_proxy()
#设置代理信息
def set_proxy():
	#设置代理信息
	print 'setting ip proxy for request....\n'
	newest_verified_proxy_ips=libhttpproxy.get_verified_proxies(30)
	verified_proxies_num=len(newest_verified_proxy_ips)
	if verified_proxies_num==0:
		config.enable_proxy=False
		logging.info('Can\' enable proxy,because no verified proxies\n')
		print 'Can\' enable proxy,because no verified proxies\n'
		return
	else:
		config.enable_proxy=True
	if config.current_proxy_index!=0 and config.current_proxy_index>=verified_proxies_num:
		config.current_proxy_index=0
	verified_proxy=newest_verified_proxy_ips[0];
	config.proxies={verified_proxy.Protocol:verified_proxy.IP+":"+str(verified_proxy.Port)}
	config.enable_proxy=True
	logging.info('Success enable proxy:'+str(config.current_proxy_index)+'\n')
	print 'Success enable proxy:'+str(config.current_proxy_index)+'\n'
#切换代理信息
def change_proxy():
	# if config.enable_proxy==False:
		# print 'didn\'t enable ip proxy,can\'t change ip proxy.'
		# return
	logging.info('change ip proxy....\n')
	print 'change ip proxy....\n'
	verified_proxies_num=libhttpproxy.get_verified_proxies_num()
	if config.current_proxy_index+1>=verified_proxies_num:
		config.current_proxy_index=0
	else:
		config.current_proxy_index=config.current_proxy_index+1
	set_proxy()
	if config.enable_proxy==True:
		logging.info('Success change ip proxy.\n' )
		print 'Success change ip proxy.\n' 
def set_logging():
	logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='chengdu_jaste.log',
	filemode='w')

def log_on(log_url):
	# files={'username':(None,'Zwcd'),'password':(None,'123456'),'redirect':(None,'https://la.gesoo.com/owner/index.php?route=common/login')}
	fields={'username':'Zwcd','password':'123456','redirect':'https://la.gesoo.com/owner/index.php?route=common/login'}
	m=MultipartEncoder(fields,boundary='my_super_custom_header')
	headers={'content-type': m.content_type,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	r,s=basic.post_form_with_session(log_url,data=m.to_string(),headers=headers)
	status_code=r.status_code
	if status_code==requests.codes.ok:
		result=urlparse.urlparse(r.url)
		params=urlparse.parse_qs(result.query,True)
		token=params["token"][0]
	
		cookies=r.cookies
		return [True,token,cookies,s]
	else:
		return [False,'',{},s]
try:
	set_proxy_enable()
	set_logging()
	log_url='https://la.gesoo.com/owner/index.php?route=common/login'
	is_log,token,cookies,req=log_on(log_url)
	if is_log==True:
		print("sucess log in")
		logging.info("sucess log in")
		order_list_url='https://la.gesoo.com/owner/index.php?route=sale/order&token='+token
		go_p_list_page(req,order_list_url,cookies=cookies)
		
		# food_url='https://la.gesoo.com/owner/index.php?route=catalog/product&token='+token
		# get_foods(food_url)
		
		# p_info='https://la.gesoo.com/owner/index.php?route=sale/order/info&order_id=135739&token='+token
		# get_product_info(req,p_info)
	else:
		print("fail log in")
		logging.info("fail log in")
	
	# go_p_list_page(p_list_url)
	#get_product_info('http://www.amazon.in/dp/B074PWHB1R/ref=s%20r_1_1014/262-4008005-9308516?s=electronics&ie=UTF8&qid=1502377276&sr=1-1014')
	#print json.dumps(get_product_info('http://www.amazon.in/dp/B074PWHB1R/ref=s%20r_1_1014/262-4008005-9308516?s=electronics&ie=UTF8&qid=1502377276&sr=1-1014'),default=model_product.productmodel2dict)
	#html=basic.get_html('http://www.amazon.in/Forme-N9-Selfie-Wireless-Mobile/dp/B071G2DSSC/ref=sr_1_142/257-5514151-9158917?s=electronics&rps=1&ie=UTF8&qid=1501400614&sr=1-142')
	#basic.html_write(html,'abc.html')
	#print html.encode('utf-8')
except BaseException as e:
	print(e)
finally:
	pass
	# db_IPProxiesPoolApplicationSwitch.update(False)