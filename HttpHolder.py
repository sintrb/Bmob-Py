# -*- coding: UTF-8 -*
'''
Modified on 2015-07-02
@author: RobinTang
@version: 1.2
@change: 添加请求方法设置

Modified on 2014-04-24
@author: RobinTang
@version: 1.1
@change: 添加对请求超时的支持

Created on 2013-10-14
HTTP请求保持
@author: RobinTang
@version: 1.0


https://github.com/sintrb/pyHttpHolder

'''

import urllib2
import cookielib
import types
import re


def urlencode(param):
    '''
    正如你所理解的URLEncode一样。
    接受字符串和字典两种类型，字典类型在Encode之后键值对(key=value)之间用&连接，字符串直接Encode
    '''
    if isinstance(param, types.DictType):
        return "&".join(("%s=%s" % (k, urllib2.quote(str(v)))
                         for k, v in param.iteritems()))
    else:
        return urllib2.quote(param)


def mkcookie(name, value, domain=''):
    '''
    创建一个Cookie
    '''
    return cookielib.Cookie(version=None, name=name, value=value, port=None, port_specified=None, domain=domain, domain_specified=None, domain_initial_dot=None,
                            path='/', path_specified=None, secure=None, expires=None, discard=None, comment=None, comment_url=None, rest=None, rfc2109=None)


def get_html_by_urldoc(doc):
    '''
    将一个urllib2.open()返回的doc读取为html文件文档(其实就是解码为字符串)
    '''
    try:
        contype = doc.info().getheader('Content-Type').lower()
    except BaseException:
        contype = 'application/x-www-form-urlencoded; charset=UTF-8'
    charset = None
    html = doc.read()
    info = doc.info()
    if ('Content-Encoding' in info and info['Content-Encoding'] == 'gzip') or (
            'content-encoding' in info and info['content-encoding'] == 'gzip'):
        # gizp
        import gzip
        import StringIO
        gz = gzip.GzipFile(fileobj=StringIO.StringIO(html))
        html = gz.read()
        gz.close()
    chs = re.findall('charset\s*=\s*([^\s,^;]*)', contype)
    if chs and len(chs) > 0:
        charset = chs[0]
    else:
        chs = re.findall('charset\s*=\s*([^\s,^;,^"]*)', html)
        if chs and len(chs) > 0:
            charset = chs[0]
    if charset:
        charset = charset.lower()
        try:
            html = html.decode(charset)
        except BaseException:
            try:
                html = html.decode('utf-8')
            except BaseException:
                try:
                    html = html.decode('gbk')
                except BaseException:
                    raise Exception('decode error!')
    return html


class HttpHolder:
    '''
    Http请求保持类
    headers, 默认的请求头，一般可以把UA之类放这
    '''

    def __init__(self, headers=None, timeout=None):
        """
        创建一个Http请求保存实例
        """
        self.headers = headers
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cj))
        self.timeout = timeout

    def open(self, url, headers=None, data=None, timeout=None, method=None):
        """
        发送一个Http请求,返回Http响应文档对象，该文档对象会保留，可通过doc成员获取
        """
        if isinstance(data, types.DictType):
            data = urlencode(data)

        if self.headers and headers:
            hd = dict(self.headers.items() + headers.items())
        elif self.headers:
            hd = self.headers
        elif headers:
            hd = headers
        else:
            hd = {}
        req = urllib2.Request(url, headers=hd)
        if method:
            req.get_method = lambda: method
        if not timeout:
            timeout = self.timeout
        if not timeout:
            doc = self.opener.open(req, data)
        else:
            doc = self.opener.open(req, data=data, timeout=self.timeout)
        self.doc = doc
        return doc

    def open_raw(self, url, headers=None, data=None,
                 timeout=None, method=None):
        '''
        原始的读取一个Http返回体
        '''
        doc = self.open(url, headers, data, timeout, method)
        return doc.read()

    def open_html(self, url, headers=None, data=None,
                  timeout=None, method=None):
        '''
        请求一个html文档（其实是请求文本类型）
        '''
        doc = self.open(url, headers, data, timeout, method)
        return get_html_by_urldoc(doc)

    def geturl(self):
        '''
        获取当前请求的响应url，在HTTP请求得到重定向时可用该方法获取实际响应的URL，该方法在多线程时不安全
        '''
        return self.doc.geturl()

    def set_cookiesdict(self, cookies):
        '''
        通过字典设置Cookie
        '''
        for (k, v) in cookies.items():
            self.cj.set_cookie(mkcookie(k, v))

    def set_cookie(self, name, value):
        '''
        设置Cookie
        '''
        self.cj.set_cookie(mkcookie(name, value))

    def get_cookiesdict(self):
        '''
        获取Cookie的字典表示
        '''
        return dict(((c.name, c.value) for c in self.cj))


if __name__ == '__main__':
    import json
    headers = {
        # Chrome User-Agent
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
    }
    # 使用Chrome的User-Agent，设置默认超时为10s
    h = HttpHolder(headers=headers, timeout=10)

    # 请求豆瓣首页并以便获取相关Cookie，该次请求使用GET方法
    h.open_html('http://www.douban.com')

    # 登陆表单
    form = {
        'email': 'abc@def.com',
        'password': '123',
        'app_name': 'radio_desktop_win',
        'version': '100'
    }
    # 尝试登陆，该次请求使用POST方法，因为data有数据，返回JSON字串
    res = h.open_html('http://www.douban.com/j/app/login',
                      headers={'Referer': 'http://www.douban.com'},
                      data=form)
    # 解析JSON
    reso = json.loads(res)
    if 'err' in reso:
        # 有错误，输出
        print reso['err']

    # 打印现在的Cookie
    print h.get_cookiesdict()
