"""This librarry will create the signed url and then able to call different functions on amazon product advertisement api
written by Pradeep Singh (pradeep.mit08@gmail.com)
"""

import hashlib,hmac, base64, time, urllib

class AmazonApi():
	def __init__(self, AccessKey, SecretKey, AssociateTag, Endpoint):
		self.AccessKey = AccessKey
		self.SecretKey = SecretKey
		self.AssociateTag = AssociateTag
		self.Endpoint = Endpoint

	def sign(self, msg):
		"""Will signthe url using sha256"""
		dig = hmac.new(self.SecretKey, msg.encode("utf-8"), hashlib.sha256).digest()
		return base64.b64encode(dig).decode()
	def itemLookup(self, keyword, category=None):
		"""Item Lookup is for create the signed URL for search in Amazon"""

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
		return signedURL
