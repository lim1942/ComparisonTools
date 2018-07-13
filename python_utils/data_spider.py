#coding=utf-8

# Author: lim
# Email: 940711277@qq.com
# Date:  2018-06-10 14:23:37

import os
import time
import json
import requests
from lxml import etree

from python_utils.login.login import get_cookies 


class spider_class:

	"""for data spider from hybase"""

	def __init__(self):
		self.path = os.path.dirname(os.path.realpath(__file__)) 
		self.cookies = self.read_cookies()
		self.ir_sitename_base = None
		self.channel_path_base = None	
		self.page = None
		self.headers = {
		"Host":"10.200.73.10:5555",
		"Connection":"keep-alive",
		"Content-Length":"284",
		"Cache-Control":"max-age=0",
		"Origin":"http://10.200.73.10:5555",
		"Upgrade-Insecure-Requests":"1",
		"Content-Type":"application/x-www-form-urlencoded",
		"User-Agent":("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKi"
			"t/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"),
		"Accept":("text/html,application/xhtml+xml,application/xml;q=0.9,image"
			"/webp,image/apng,*/*;q=0.8"),
		"Referer":"http://10.200.73.10:5555/admin/protected/main.do",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-CN,zh;q=0.9",
		}


	def read_cookies(self):
		cookie_dir = os.path.join(os.sep.join([self.path,'login']),'cookies.txt')
		with open(cookie_dir) as f:
			cookies = f.read()
		cookies = eval(cookies)
		return cookies


	def flush_cookies(self):
		toggle = False	
		while not toggle:
			toggle = get_cookies()
		self.cookies = self.read_cookies()
		print('successful flush cookies !!!')


	def out_spider(self):

		# for out spider
		url = 'http://10.200.73.10:5555/admin/protected/main.do'
		params = {
		"p":"rec",
		"dbname":"website_formal_20160321",
		"searchopt":"hybase;false;false;true;trs;false;null;null",
		"outlinefields":"DOCPUBTIME",
		"searchexpr":"IR_SITENAME:{} AND DOCCHANNEL:{}".format(
					self.ir_sitename_base,self.channel_path_base),
		'pageno':str(self.page),
		"sortexpr":"-DOCPUBTIME",		
		}	
		out_retry = 5	
		while out_retry:
			try:
				r = requests.post(url,headers=self.headers,
							cookies=self.cookies,data=params)
				if r.status_code == 200 and len(r.text)>6000:
					return r.text
				else:
					raise Exception('out status_code error...')
			except Exception as e:
				out_retry -=1
				time.sleep(1)
				self.flush_cookies()
				print (e,'retry:{}'.format(out_retry))


	def out_parse(self):

		out_page = self.out_spider()
		if not out_page:
			return None

		xml = etree.HTML(out_page)
		recordid_list = xml.xpath("//input[@name='uuid']/@value")
		return recordid_list


	def inner_spider(self):

		recordid_list = self.out_parse()
		if recordid_list is None:
			return None

		inner_page_list = []
		inner_url = 'http://10.200.73.10:5555/admin/protected/main.do'

		for recordid in recordid_list:
			params = {
			"p":"rec",
			"colname":"",
			"page":"record_detail.jsp",
			"dbname":"website_formal_20160321",
			"searchexpr":"IR_SITENAME:{} AND DOCCHANNEL:{}".format(
				self.ir_sitename_base,self.channel_path_base),
			"sortexpr":"-DOCPUBTIME",
			"cutsize":"65536",
			"pageno":str(self.page),
			"pagesize":"10",
			"searchopt":"hybase;false;false;true;trs;false;null;null",
			"recordid":recordid,
			"docid":"2",
			}

			inner_try = 5
			while  inner_try:
				try:
					r = requests.post(inner_url,headers=self.headers,cookies=self.cookies,data=params)
					if r.status_code == 200 and len(r.text)>6000:
						inner_page_list.append(r.text)
						break
					else:
						raise Exception('inner status_code error 1')
				except Exception as e:
					inner_try -=1
					time.sleep(1)
					self.flush_cookies()
					print(e,'inner_try：{}'.format(inner_try))

		return inner_page_list


	def inner_parse(self):
		data = {"data":[],"message":"查询成功"}
		inner_page_list = self.inner_spider()
		if inner_page_list is None:
			data['message'] = '查询失败'
			return data

		for inner_page in inner_page_list:

			item = {}
			inner_page_xml = etree.HTML(inner_page)
			tr_list = inner_page_xml.xpath("//table/tbody/tr")
			for tr in tr_list:
				try:
					td_1_text = tr.xpath("./td[1]")[0].xpath('string(.)').strip()
				except:
					continue
				
				if 'DOCTITLE' in td_1_text:
					try:
						item['DOCTITLE'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['DOCTITLE'] = ''
			
				if 'DOCPUBTIME' in td_1_text:
					try:
						item['DOCPUBTIME'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['DOCPUBTIME'] = ''

				if 'IR_SRCNAME' in td_1_text:
					try:
						item['IR_SRCNAME'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['IR_SRCNAME'] = ''

				if 'PUBURL' in td_1_text:
					try:
						item['PUBURL'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['PUBURL'] = ''

				if 'IR_CONTENT' in td_1_text:
					try:
						item['IR_CONTENT'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['IR_CONTENT'] =''

				if 'DOCAUTHOR' in td_1_text:
					try:
						item['DOCAUTHOR'] = tr.xpath("./td[2]")[0].xpath('string(.)').strip()
					except:
						item['DOCAUTHOR'] = ''

			data['data'].append(item)

		return data
														 

	def back_data(self,ir_sitename_base,channel_path_base,page):

		self.ir_sitename_base = ir_sitename_base
		self.channel_path_base = channel_path_base
		self.page = page

		data = self.inner_parse()
		data = json.dumps(data)
		data = data.encode('utf-8')
		return data






# --------------------- for out import-------------------------- 
spider_ob = spider_class()
def get_data(ir_sitename_base, channel_path_base, page):

	data = spider_ob.back_data(ir_sitename_base, channel_path_base, page)
	return data