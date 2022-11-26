import os
import uuid
from publisher import Publisher
import ujson
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from logger import configure_logging


define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/appeal", AppealHandler),
        ]
        settings = dict(
            title="Форма обращений",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret=uuid.uuid4().int,
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("appeal.html")


class AppealHandler(tornado.web.RequestHandler):
    async def post(self):
        last_name = self.get_argument("last_name", default=None, strip=False)
        first_name = self.get_argument("first_name", default=None, strip=False)
        patronymic = self.get_argument("patronymic", default=None, strip=False)
        phone_number = self.get_argument("phone_number", default=None, strip=False)
        appeal = self.get_argument("appeal", default=None, strip=False)
        data = {
            'last_name': last_name,
            'first_name': first_name,
            'patronymic': patronymic,
            'phone_number': phone_number,
            'appeal': appeal
        }

        payload = ujson.dumps(data)
        sender.publish(body=payload)
        self.render("appeal.html")


if __name__ == "__main__":
    configure_logging()
    sender = Publisher()
    sender.connect_to_channel()
    sender.setup_exchange()
    sender.queue_bind()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
