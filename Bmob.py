# -*- coding: UTF-8 -*
'''
Created on 2015年7月2日

@author: RobinTang

https://github.com/sintrb/Bmob-Py

'''
import json
import copy
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
        self.http = HttpHolder(
            headers={
                "X-Bmob-Application-Id": appid,
                "X-Bmob-REST-API-Key": restkey,
                "Content-Type": "application/json"})

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
        self.w = {}  # where
        self.items = None

    def copy(self):
        q = Query(self.clz, self.context)
        q.q = copy.deepcopy(self.q)
        q.w = copy.deepcopy(self.w)
        return q

    def get_urlencode(self):
        if self.w:
            self.q['where'] = json.dumps(self.w)
        elif 'where' in self.q:
            del self.q['where']
        return urlencode(self.q)

    def order(self, o):
        self.q['order'] = o
        return self.copy()

    def limit(self, l):
        self.q['limit'] = l
        return self.copy()

    def skip(self, s):
        self.q['skip'] = s
        return self.copy()

    def count(self):
        if not self.items is None:
            return len(self.items)
        else:
            self.limit(0)
            self.q['count'] = 1
            return json.loads(self.context.http.open_html(
                '/'.join([self.context.apiurl, self.clz.__name__, '?' + self.get_urlencode()])))['count']

    def get_kw(self, k):
        if k in self.w:
            return self.w[k]
        else:
            self.w[k] = {}
            return self.w[k]

    def w_eq(self, k, v):
        '''less then'''
        self.w[k] = v
        return self.copy()

    def w_lt(self, k, v):
        '''less then'''
        self.get_kw(k)['$lt'] = v
        return self.copy()

    def w_lte(self, k, v):
        '''less then'''
        self.get_kw(k)['$lte'] = v
        return self.copy()

    def w_gt(self, k, v):
        '''less then'''
        self.geet_kw(k)['$gt'] = v
        return self.copy()

    def w_gt(self, k, v):
        '''less then'''
        self.get_kw(k)['$gte'] = v
        return self.copy()

    def w_ne(self, k, v):
        '''less then'''
        self.get_kw(k)['$ne'] = v
        return self.copy()

    def w_in(self, k, v):
        '''less then'''
        self.get_kw(k)['$in'] = v
        return self.copy()

    def w_nin(self, k, v):
        '''less then'''
        self.get_kw(k)['$nin'] = v
        return self.copy()

    def w_exists(self, k, v):
        '''less then'''
        self.get_kw(k)['$exists'] = v
        return self.copy()

    def w_select(self, k, v):
        '''less then'''
        self.get_kw(k)['$select'] = v
        return self.copy()

    def w_dontSelect(self, k, v):
        '''less then'''
        self.get_kw(k)['$dontSelect'] = v
        return self.copy()

    def w_all(self, k, v):
        '''less then'''
        self.get_kw(k)['$all'] = v
        return self.copy()

    def w_regex(self, k, v):
        '''less then'''
        self.get_kw(k)['$regex'] = v
        return self.copy()

    def exec_query(self):
        rs = []
        for r in json.loads(self.context.http.open_html(
                '/'.join([self.context.apiurl, self.clz.__name__, '?' + self.get_urlencode()])))['results']:
            rs.append(self.clz(**r))
        self.items = rs
        return self.items

    def first(self):
        q = self.copy()
        q.limit(1)
        rs = q.exec_query()
        return len(rs) and rs[0] or None

    def __getslice__(self, s, e):
        if self.items is None:
            self.exec_query()
        return self.items.__getslice__(s, e)

    def __iter__(self):
        if self.items is None:
            self.exec_query()
        return iter(self.items)

    def __getitem__(self, k):
        if self.items is None:
            self.exec_query()
        return self.items.__getitem__(k)

    def __len__(self):
        return self.count()


class BmobModel(object):
    '''
    Basic Bmob model, all other Bmob model must inherit this class.
    '''

    def __init__(self, context=None, objectId=None, **kwargs):
        super(BmobModel, self).__init__()
        # check objectId
        if isinstance(context, str):
            objectId = context
            context = None

        if not context:
            context = BmobSDK.context
        if not context:
            raise BaseException("No BmobSDK context setuped!")
        self.context = context
        self.objectId = objectId
        if self.objectId:
            # get object by id
            for k, v in json.loads(self.context.http.open_html(
                    '/'.join([self.context.apiurl, self.get_modelname(), self.objectId]))).items():
                setattr(self, k, v)
        else:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def get_attrs(self):
        return [k for k in type(self).__dict__ if not k.startswith('__')]

    def get_dict(self):
        ks = self.get_attrs()
        clz = type(self)
        dic = {}
        tps = [
            type(v) for v in [
                1, 1, 1.0, '1', (1, 2), [
                    1, 2], {
                    '1': '1'}, {
                    1, 2}]]
        return dict([(k, type(getattr(clz, k))(getattr(self, k)))
                     for k in ks if type(getattr(clz, k)) in tps])

    def get_modelname(self):
        return type(self).__name__

    def save(self):
        data = self.get_dict()
        jdata = json.dumps(data)
        if self.objectId:
            for k, v in json.loads(self.context.http.open_html(
                    '/'.join([self.context.apiurl, self.get_modelname(), self.objectId]), data=jdata, method="PUT")).items():
                setattr(self, k, v)
        else:
            for k, v in json.loads(self.context.http.open_html(
                    '/'.join([self.context.apiurl, self.get_modelname()]), data=jdata)).items():
                setattr(self, k, v)

    def delete(self):
        if self.objectId:
            res = json.loads(self.context.http.open_html(
                '/'.join([self.context.apiurl, self.get_modelname(), self.objectId]), method="DELETE"))['msg'] == 'ok'
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
        name = ''  # string
        score = 1.0  # number

    # setup BmobSDK
    BmobSDK.setup('77b5dad35e17a087d679e62db9936950',
                  'a9ab631355ce61f19be22f55a0b1b422')

    # create a course and save it
    c1 = Course(name="Python 2.x Program", score=4)
    c1.save()

    # get course of id '957638ab1e'
    c2 = Course('957638ab1e')
    print '%s : %s' % (c2.name, c2.score)
    c2.score = c2.score + 1
    c2.save()

    # Query:
    # print the course count
    print 'count of courses : %d' % Course().query().count()  # or Query(Course).count()

    # create a Course query and query all contain "Program" courses
    for c in Course().query().w_regex('name', 'Program').order("-createdAt").limit(20):
        print '%s  %s : %s' % (c.createdAt, c.name, c.score)

    # query like a list
    q = Course().query().skip(5).limit(10)
    print 'Items of q:'
    for c in q:
        print '\t', c.objectId
    print "q.count() : %d" % q.count()
    print q[-1].name
    print q[3:]

    # delete
    print 'count before delete: %d' % len(Course().query())
    c1.delete()
    print 'count after delete: %d' % len(Course().query())
