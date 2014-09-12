import tornado.web
import tornado.escape
import tornado.template
from pymongo import MongoClient
from tools import getTemplate


class AdminHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.mongoConn=MongoClient()['docdatabase']

    def get(self):
        urls = self.mongoConn['urls'].find({},{'_id':False})
        url_list=[]
        for url in urls:
            doc = self.mongoConn['docs'].find({'_id':url['doc']})
            title = doc[0]['title']
            url_dict={}
            url_dict['url']=("{0}://{1}/get/{2}".format(self.request.protocol,self.request.host,url['url']))
            url_dict['title']=title
            url_list.append(url_dict)
        html = getTemplate('list_urls.html',urls=url_list)
        self.write(html)