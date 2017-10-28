"""This librarry will create the signed url and then able to call different functions on amazon product advertisement api
written by Pradeep Singh (pradeep.mit08@gmail.com)
"""

import hashlib,hmac, base64, time, urllib, urllib2
import traceback
import xml.etree.ElementTree as ET

class AmazonApi():
	def __init__(self, AccessKey, SecretKey, AssociateTag, Endpoint):
		self.AccessKey = AccessKey
		self.SecretKey = SecretKey
		self.AssociateTag = AssociateTag
		self.Endpoint = Endpoint
		self.RecordList = []
		self.productList = []
		self.AmazonString = "{http://webservices.amazon.com/AWSECommerceService/2011-08-01}"

	def sign(self, msg):
		"""Will signthe url using sha256"""
		dig = hmac.new(self.SecretKey, msg.encode("utf-8"), hashlib.sha256).digest()
		return base64.b64encode(dig).decode()
	def makeRequest(self, url):
		"""Used to make http request and return the response
		parameters:
		@url Signed url to get information from Amazon
		return xml data
		"""
		request = urllib2.Request(url)

		try: 
			response = urllib2.urlopen(request)
			return response
		except urllib2.HTTPError, e:
			return 'HTTPError = ' + str(e.code)
		except urllib2.URLError, e:
			return 'URLError = ' + str(e.reason)
		except httplib.HTTPException, e:
			return 'HTTPException'
		except Exception:
			print 'generic exception: ' + traceback.format_exc()

	def getProductData(self, xml_node):
		AmazonString = self.AmazonString
		for child in xml_node:
			itemDetail = {'DetailPageURL':'', 'ASIN': '', 'SmallImage':{}, 'MediumImage': {}, 'Binding': '', 'Brand': '', 'Color': '', 'ListPrice': {}, 'Manufacturer': '', 'Model': '','Title': '', 'SalePrice':{}}
			if child.tag == AmazonString + "Item":
				for c in child:
					if c.tag == AmazonString + "DetailPageURL":
						itemDetail['DetailPageURL'] = c.text
					if c.tag == AmazonString + "ASIN":
						itemDetail['ASIN'] = c.text

					if c.tag == AmazonString + "SmallImage":
						for imgAttr in c:
							if imgAttr.tag == AmazonString + "URL":
								itemDetail['SmallImage']["URL"] = imgAttr.text
							if imgAttr.tag == AmazonString + "Height":
								itemDetail['SmallImage']["Height"] = imgAttr.text
							if imgAttr.tag == AmazonString + "Width":
								itemDetail['SmallImage']["Width"] = imgAttr.text

					if c.tag == AmazonString + "MediumImage":
						for imgAttr in c:
							if imgAttr.tag == AmazonString + "URL":
								itemDetail['MediumImage']["URL"] = imgAttr.text
							if imgAttr.tag == AmazonString + "Height":
								itemDetail['MediumImage']["Height"] = imgAttr.text
							if imgAttr.tag == AmazonString + "Width":
								itemDetail['MediumImage']["Width"] = imgAttr.text

					if c.tag == AmazonString + "ItemAttributes":
						for itemAttr in c:
							if itemAttr.tag == AmazonString + "Binding":
								itemDetail['Binding'] = itemAttr.text
							if itemAttr.tag == AmazonString + "Brand":
								itemDetail['Brand'] = itemAttr.text
							if itemAttr.tag == AmazonString + "Color":
								itemDetail['Color'] = itemAttr.text
							if itemAttr.tag == AmazonString + "ListPrice":
								for priceAttr in itemAttr:
									if priceAttr.tag == AmazonString + "Amount":
										itemDetail['ListPrice']['Amount'] = priceAttr.text
									if priceAttr.tag == AmazonString + "CurrencyCode":
										itemDetail['ListPrice']['CurrencyCode'] = priceAttr.text
									if priceAttr.tag == AmazonString + "FormattedPrice":
										itemDetail['ListPrice']['FormattedPrice'] = priceAttr.text
							if itemAttr.tag == AmazonString + "Manufacturer":
								itemDetail["Manufacturer"] = itemAttr.text
							if itemAttr.tag == AmazonString + "Model":
								itemDetail["Model"] = itemAttr.text
							if itemAttr.tag == AmazonString + "Title":
								itemDetail["Title"] = itemAttr.text
					if c.tag == AmazonString + "OfferSummary":
						for offer in c:
							if offer.tag == AmazonString + "LowestNewPrice":
								for salePriceAttr in offer:
									if salePriceAttr.tag == AmazonString + "Amount":
										itemDetail['SalePrice']['Amount'] = salePriceAttr.text
									if salePriceAttr.tag == AmazonString + "CurrencyCode":
										itemDetail['SalePrice']['CurrencyCode'] = salePriceAttr.text
									if salePriceAttr.tag == AmazonString + "FormattedPrice":
										itemDetail['SalePrice']['FormattedPrice'] = salePriceAttr.text
			if(len(itemDetail['Title']) > 0):
				print'itemDetail=',itemDetail
				self.RecordList.append(itemDetail)
			self.getProductData(child)




							



	def get_data_from(self, xml_node):
		AmazonString = self.AmazonString
		# print'nodes===',xml_node
		# Loop over the children of current node
		
		for child in xml_node:
			# item = {'ASIN': '', 'ParentASIN':'',  'Manufacturer':'','ProductGroup': '', 'Title':''}
			# print'child=========',child
			# To avoid the "Category" Node, we only check the ones who have exactly 2 children
			if child.tag == AmazonString + "Item":
				# Looping over the children of a BrowseNode node,
				# we simply print the contents (.text)
				for c in child:
					# if c.tag == AmazonString + "ItemAttributes":
					# 	for attr in c:
					# 		if attr.tag == AmazonString + "Manufacturer":
					# 			print("Manufacturer : " + attr.text)
					# 			item['Manufacturer'] = attr.text
					# 		if c.tag == AmazonString + "ProductGroup":
					# 			print("ProductGroup: " + c.text)
					# 			item['ProductGroup'] = attr.text
					# 		if attr.tag == AmazonString + "Title":
					# 			print("Title: " + attr.text)
					# 			item['Title'] = attr.text

					if c.tag == AmazonString + "ASIN":
						print("ASIN : " + c.text)
						# item['ASIN'] = c.text
						self.productList.append(c.text)

					# if c.tag == AmazonString + "ParentASIN":
					# 	print("ParentASIN: " + c.text)
					# 	item['ParentASIN'] = c.text
			# if(len(item['Title']) > 0):
			# 	self.RecordList.append(item)
			self.get_data_from(child)


	def itemLookup(self, ProductID = []):
		
		RequestURI = "/onca/xml"
		urlParams = dict(
			Service = 'AWSECommerceService',
			Operation = 'ItemLookup',
			AssociateTag = self.AssociateTag,
			SubscriptionId = self.AccessKey,
			IdType='ASIN',
			ResponseGroup='Images,ItemAttributes,Offers'
			)
		for item in self.productList:
			urlParams['ItemId'] = item
			urlParams['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
			keys = urlParams.keys()
			keys.sort()
			# map the values in same order
			values = map(urlParams.get, keys)

			urlString = urllib.urlencode(zip(keys,values))

			string_to_sign = "GET\n%s\n%s\n%s"%(self.Endpoint, RequestURI, urlString)
			signature = self.sign(string_to_sign)
			signature = urllib.urlencode({'Signature':signature})
			signedURL = "http://"+self.Endpoint + RequestURI +"?"+ urlString + "&" + signature
			content = self.makeRequest(signedURL)
			root=ET.fromstring(content.read())
			self.getProductData(root)


	def itemSearch(self, keyword, category=None):
		"""Item search is for create the signed URL for search in Amazon"""

		Endpoint = self.Endpoint
		RequestURI = "/onca/xml"
		urlParams = dict(
			Service = 'AWSECommerceService',
			Operation = 'ItemSearch',
			AssociateTag = self.AssociateTag,
			AWSAccessKeyId = self.AccessKey

		)

		if not category and len(category > 3):
			urlParams['SearchIndex'] = 'All'
		else:
			urlParams['SearchIndex'] = category

		if keyword and len(keyword) > 0:
			urlParams['Keywords'] = keyword
		else:
			return
		urlParams['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
		#sort Parameters
		keys = urlParams.keys()
		keys.sort()
		# map the values in same order
		values = map(urlParams.get, keys)

		Sortedparameter = zip(keys,values)

		#can not done with urlencode because it convert space to +
		url_string = ''
		count=0;
		for k,v in Sortedparameter:
			tmp = "%s=%s"%(k,urllib.quote(v))
			if count == 0:
				url_string += tmp
			else:
				url_string += "&"+tmp
			count+=1

		string_to_sign = "GET\n%s\n%s\n%s"%(Endpoint, RequestURI, url_string)

		signature = self.sign(string_to_sign)
		signature = urllib.urlencode({'Signature':signature})
		print('unsigned Url =',"http://"+Endpoint+RequestURI+"?" + url_string +"&"+ urllib.urlencode({'Signature':signature}))
		signedURL = "http://"+Endpoint + RequestURI +"?"+ url_string + "&" + signature
		print('Signed url=',signedURL)
		content = self.makeRequest(signedURL)
		# print'content==',content.read()
		root=ET.fromstring(content.read())
		self.RecordList = []
		self.productList = []
		self.get_data_from(root)
		print'self.list',self.productList
		self.itemLookup()
		print'self.list',self.RecordList
		return self.RecordList
