import tornado.ioloop
import tornado.web


from controllers import DataHandler,ReturnHandler,DownloadHandler



application = tornado.web.Application([
    (r'/create/',DataHandler),
    (r'/get/(.*)', ReturnHandler),
    (r'/download/(.*)', DownloadHandler),
])

if __name__=='__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()