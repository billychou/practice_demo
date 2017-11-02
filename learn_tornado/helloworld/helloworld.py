#!-*-coding:utf-8-*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


def make_app():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    return application


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()




