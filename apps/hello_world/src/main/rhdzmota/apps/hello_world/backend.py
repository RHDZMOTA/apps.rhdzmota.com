from rhdzmota.ext.streamlit_webapps.backend import BackendRequestHandler


class HelloEndpoint(BackendRequestHandler):
    alias="hello"

    def get(self):
        self.write({'message': 'hello world'})


def get_handler():
    return HelloEndpoint

