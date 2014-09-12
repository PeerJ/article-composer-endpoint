import tornado.web
import tornado.escape
import tornado.template
import json
from pymongo import MongoClient
from bson.binary import Binary
from tools import urlgenerator


class DataHandler(tornado.web.RequestHandler):


    def initialize(self):
        self.mongoConn=MongoClient()['docdatabase']

    def post(self):

        file_list = []
        args_dict = {}

        ##Get All Files
        for files,content in self.request.files.iteritems():
            fileid = self.mongoConn['files'].insert({'filename':[content[0]['filename']],'body':Binary(content[0]['body']),'content_type':content[0]['content_type']})
            file_list.append({'filename':[content[0]['filename']],'fileid':fileid})

        ##Get Arguments

        args = self.get_argument('article',None)

        args_dict = json.loads(args)
        if "_id" in args_dict:
            doc_id=args_dict['_id']
            args_dict['doc_id']=doc_id
            del args_dict['_id']

        for key in args_dict:
            print key

        if not args_dict:
            raise tornado.web.HTTPError(400,'No Data Found')

        ##Form Stored Data
        store_data = args_dict
        ##Add Files
        store_data['files']=file_list
        ##Store Data in Mongo
        docid=self.mongoConn['docs'].insert(store_data)
        ##Generate Random URL
        uri=urlgenerator.url_generator()
        ##Save in DB
        url_data={'url':uri,'doc':docid}
        self.mongoConn['urls'].insert(url_data)

        ##Display URL
        url="{0}://{1}/get/{2}".format(self.request.protocol,self.request.host,uri)
        self.set_header("Access-Control-Allow-Origin",'*')
        self.write(json.dumps({"URL":"{0}".format(url)}))