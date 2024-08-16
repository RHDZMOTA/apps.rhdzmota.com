import gc
from functools import cache

from tornado.web import Application, RequestHandler
from tornado.routing import Rule, PathMatches


@cache
def get_tornado_application_instance():
    import gc

    return next(o for o in gc.get_referrers(Application) if o.__class__ is Application)


def register_backend_handler(uri: str, handler):
    tornado_app = get_tornado_application_instance()
    tornado_app.wildcard_router.rules.insert(0, Rule(PathMatches(uri), handler))


# https://discuss.streamlit.io/t/streamlit-restful-app/409/19
class HelloHandler(RequestHandler):
    def get(self):
        self.write({'message': 'hello world'})

    @classmethod
    def register(cls, page_endpoint: str):
        register_backend_handler(f"/api/{page_endpoint}", cls)


def register_handlers(page_endpoint: str):
    HelloHandler.register(page_endpoint=page_endpoint)
