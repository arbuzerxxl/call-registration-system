import logging
import uuid
import ujson
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from publisher import Publisher


# LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -10s %(lineno) -5d: %(message)s -10s')
# LOGGER = logging.getLogger(__name__)

def configure_logging():

    global logger

    logger = logging.getLogger('TornadoLog')
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
        fmt='%(levelname) -10s [%(asctime)s] %(name) -15s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S'
    )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


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
            debug=False,
        )
        super(Application, self).__init__(handlers, **settings)


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

        logger.info("Получение данных из формы..")

        data = ujson.loads(self.request.body)

        message = f"Получены данные: " \
                  f" -Имя: {data['first_name']}" \
                  f" -Фамилия: {data['last_name']}" \
                  f" -Отчество: {data['patronymic']}" \
                  f" -Номер телефона: {data['phone_number']}" \
                  f" -Обращение: {data['appeal']}"

        logger.info(msg=message)

        publisher.publish(body=self.request.body)
        self.set_status(200)


def main():

    global publisher

    configure_logging()
    publisher = Publisher()
    try:
        publisher.run()
        app = Application()
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        publisher.disconnect()
    except Exception:
        publisher.disconnect()


if __name__ == "__main__":
    main()
