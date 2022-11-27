import os
import uuid
from publisher import Publisher
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from logger import configure_logging


define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/appeal", AppealHandler),
        ]
        settings = dict(
            title="Форма обращений",
            xsrf_cookies=False,
            cookie_secret=uuid.uuid4().int,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


# class MainHandler(tornado.web.RequestHandler):
#     async def get(self):
#         self.render("appeal.html")


class AppealHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):

        super(AppealHandler, self).__init__(*args, **kwargs)
        self.set_header('Cache-Control',
                        'no-store, no-cache, must-   revalidate, max-age=0')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, PUT, DELETE, OPTIONS')

    def options(self, *args):
        self.set_status(204)
        self.finish()

    async def post(self):

        # добавить логи для json
        publisher.publish(body=self.request.body)
        self.set_status(200)
        # self.render("appeal.html")


if __name__ == "__main__":
    configure_logging()
    publisher = Publisher()
    publisher.connect_to_channel()
    publisher.setup_exchange()
    publisher.setup_queue()
    publisher.queue_bind()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
