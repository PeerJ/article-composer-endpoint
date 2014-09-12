import tornado.web
import tornado.escape
import tornado.template
from pymongo import MongoClient
from tools import getTemplate
import json

class ReturnHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.mongoConn=MongoClient()['docdatabase']

    def get(self,urlid):
        doc = self.mongoConn['urls'].find_one({'url':urlid},{'doc':True,'_id':False})
        if doc==None:
            raise tornado.web.HTTPError(404,'Not Found')
        docdata = self.mongoConn['docs'].find_one({'_id':doc['doc']},{'_id':False})
        files = docdata['files']
        for docfiles in files:
            download_url="{0}://{1}/download/{2}".format(self.request.protocol,self.request.host,docfiles['fileid'])
            docfiles['download_url']=download_url
        del docdata['files']
        authors = docdata['authors']
        del docdata['authors']
        funders = docdata['funders']
        del docdata['funders']
        contributions = docdata['contributions']
        del docdata['contributions']
        affiliations = docdata['affiliations']
        del docdata['affiliations']
        terms = docdata['terms']
        del docdata['terms']


        html = getTemplate('show_doc.html',data=docdata,files=files,authors=authors,funders=funders,contributions=contributions,affiliations=affiliations,terms=terms)
        self.write(html)
