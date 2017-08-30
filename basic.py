#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import logging
import io
import codecs
import requests
from lxml import etree

import config

def get_html_with_session(req,url,proxies={},cookies={}):
	headers = {'content-type': 'application/json','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	r=''
	try:
		if config.enable_proxy==False:
			r=req.get(url,headers=headers,timeout=15,cookies=cookies,verify=False)
		else:
			r=req.get(url,headers=headers,proxies=proxies if len(proxies)>0 else config.proxies,timeout=15,cookies=cookies,verify=False)
	except  requests.exceptions.ConnectionError as e:
		raise e
	except  requests.Timeout as e:
		raise e
	print(r.status_code)
	return r
def post_form_with_session(url,headers={},data={},proxies={},cookies={},files={}):
	tempheaders =headers if len(headers)>0 else {'content-type': 'multipart/form-data;boundary=----WebKitFormBoundaryX9Zq35pVDOqGBiBm','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	r=''
	try:
		s=requests.Session()
		if config.enable_proxy==False:
			r=s.post(url,headers=tempheaders,data=data,timeout=15,verify=False,cookies=cookies,files=files)
		else:
			r=s.post(url,headers=tempheaders,data=data, verify=False,proxies=proxies if len(proxies)>0 else config.proxies,timeout=15,cookies=cookies,files=files)
	except  requests.exceptions.ConnectionError as e:
		raise e
	except  requests.Timeout as e:
		raise e
	return r,s
	
def use_proxy(enable_proxy,proxy_url):
	proxy_handler=urllib2.ProxyHandler({"http",proxy_url})
	null_proxy_handler=urllib2.ProxyHandler({})
	if config.enable_proxy:
		opener=urllib2.build_opener(proxy_handler)
	else:
		opener=urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)

def html_write(html,filename):
	with codecs.open(filename,'w','utf-8') as f:
		f.write(html)