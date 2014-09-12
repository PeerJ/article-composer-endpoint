import tornado.web
import tornado.escape
import tornado.template
from pymongo import MongoClient
from bson.objectid import ObjectId

class DownloadHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.mongoConn=MongoClient()['docdatabase']

    def get(self,fileid):
        fileid = ObjectId(fileid)
        filedata = self.mongoConn['files'].find_one({'_id':fileid})
        if filedata==None:
            raise tornado.web.HTTPError(404,'Not Found')
        self.set_header("Content-Type", filedata['content_type'])
        self.set_header("Content-Disposition", "attachment; filename={0}".format(filedata['filename'][0]))
        self.write(filedata['body'])

