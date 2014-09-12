import tornado.ioloop
import tornado.web


from controllers import DataHandler,ReturnHandler,DownloadHandler,AdminHandler



application = tornado.web.Application([
    (r'/create/',DataHandler),
    (r'/get/(.*)', ReturnHandler),
    (r'/download/(.*)', DownloadHandler),
    (r'/list/', AdminHandler),
])

if __name__=='__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()