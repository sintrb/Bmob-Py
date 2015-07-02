# -*- coding: UTF-8 -*
'''
Created on 2015年7月2日

@author: RobinTang

https://github.com/sintrb/Bmob-Py

'''
import json
from HttpHolder import HttpHolder, urlencode

class BmobSDK(object):
	'''
	BmobSDK, create with Application ID and REST API Key. You can use she same Application with BmobSDK.setup() method.
	'''
	context = None
	def __init__(self, appid, restkey, apiurl='https://api.bmob.cn/1/classes'):
		super(BmobSDK, self).__init__()
		self.appid = appid
		self.restkey = restkey
		self.apiurl = apiurl
		self.http = HttpHolder(headers={"X-Bmob-Application-Id":appid, "X-Bmob-REST-API-Key":restkey, "Content-Type":"application/json"})

	@staticmethod
	def setup(appid, restkey):
		BmobSDK.context = BmobSDK(appid, restkey)

class Query(object):
	'''
	Bmob Query
	'''
	def __init__(self, clz, context=None):
		super(Query, self).__init__()
		if not context:
			context = BmobSDK.context
		if not context:
			raise BaseException("No BmobSDK context setuped!")
		self.context = context
		self.clz = clz
		self.q = {}
		self.w = {}	# where

	def get_urlencode(self):
		if self.w:
			self.q['where'] = json.dumps(self.w)
		elif 'where' in self.q:
			del self.q['where']
		return urlencode(self.q)

	def order(self, o):
		self.q['order'] = o
		return self
	def limit(self, l):
		self.q['limit'] = l
		return self
	def skip(self, s):
		self.q['skip'] = s
		return self
	def count(self):
		self.limit(0)
		self.q['count'] = 1
		return json.loads(self.context.http.open_html('/'.join([self.context.apiurl, self.clz.__name__, '?'+self.get_urlencode()])))['count']

	def get_kw(self, k):
		if k in self.w:
			return self.w[k]
		else:
			self.w[k] = {}
			return self.w[k]
	def w_eq(self, k, v):
		'''less then'''
		self.w[k] = v
		return self
	def w_lt(self, k, v):
		'''less then'''
		self.get_kw(k)['$lt'] = v
		return self
	def w_lte(self, k, v):
		'''less then'''
		self.get_kw(k)['$lte'] = v
		return self
	def w_gt(self, k, v):
		'''less then'''
		self.geet_kw(k)['$gt'] = v
		return self
	def w_gt(self, k, v):
		'''less then'''
		self.get_kw(k)['$gte'] = v
		return self
	def w_ne(self, k, v):
		'''less then'''
		self.get_kw(k)['$ne'] = v
		return self
	def w_in(self, k, v):
		'''less then'''
		self.get_kw(k)['$in'] = v
		return self
	def w_nin(self, k, v):
		'''less then'''
		self.get_kw(k)['$nin'] = v
		return self
	def w_exists(self, k, v):
		'''less then'''
		self.get_kw(k)['$exists'] = v
		return self
	def w_select(self, k, v):
		'''less then'''
		self.get_kw(k)['$select'] = v
		return self
	def w_dontSelect(self, k, v):
		'''less then'''
		self.get_kw(k)['$dontSelect'] = v
		return self
	def w_all(self, k, v):
		'''less then'''
		self.get_kw(k)['$all'] = v
		return self
	def w_regex(self, k, v):
		'''less then'''
		self.get_kw(k)['$regex'] = v
		return self

	def __getslice__(self, s, e):
		self.skip(s)
		self.limit(e-s+1)
		return self.__iter__()
	def __iter__(self):
		rs = []
		for r in json.loads(self.context.http.open_html('/'.join([self.context.apiurl, self.clz.__name__, '?'+self.get_urlencode()])))['results']:
			rs.append(self.clz(**r))
		return iter(rs)


class BmobModel(object):
	'''
	Basic Bmob model, all other Bmob model must inherit this class.
	'''
	def __init__(self, context=None, **kwargs):
		super(BmobModel, self).__init__()
		if not context:
			context = BmobSDK.context
		if not context:
			raise BaseException("No BmobSDK context setuped!")
		self.context = context
		self.objectId = None
		for k,v in kwargs.items():
			setattr(self, k, v)
	def get_attrs(self):
		return [k for k in type(self).__dict__ if not k.startswith('__')]
	def get_dict(self):
		ks = self.get_attrs()
		clz = type(self)
		return dict([(k,type(getattr(clz, k))(getattr(self, k))) for k in ks])
	def get_modelname(self):
		return type(self).__name__
	def save(self):
		data = self.get_dict()
		jdata = json.dumps(data)
		if self.objectId:
			for k,v in json.loads(self.context.http.open_html('/'.join([self.context.apiurl, self.get_modelname(), self.objectId]), data=jdata, method="PUT")).items():
				setattr(self, k, v)
		else:
			for k,v in json.loads(self.context.http.open_html('/'.join([self.context.apiurl, self.get_modelname()]), data=jdata)).items():
				setattr(self, k, v)
	def delete(self):
		if self.objectId:
			res = json.loads(self.context.http.open_html('/'.join([self.context.apiurl, self.get_modelname(), self.objectId]), method="DELETE"))['msg']=='ok'
			if res:
				self.objectId = None
			return res
		else:
			return True
	def query(self):
		return Query(type(self))

if __name__ == '__main__':
	# from Bmob import BmobSDK, BmobModel

	# define a Model
	class Course(BmobModel):
		name = ''	# string
		score = 1.0	# number

	# setuo BmobSDK
	BmobSDK.setup('77b5dad35e17a087d679e62db9936950', 'a9ab631355ce61f19be22f55a0b1b422')

	# create a course and save it
	c = Course(name="Python 2.x Program", score=4)
	c.save()

	# print the course count
	print Course().query().count()

	# create a Course query and query all contain "Program" courses
	for c in Course().query().w_regex('name','Program').order("-createdAt").limit(20):
		print '%s  %s : %s'%(c.createdAt, c.name, c.score)
		if c.score == 4:
			c.delete()	# test delete, delete the object which created just.
