from rhdzmota.ext.streamlit_webapps.backend import BackendRequestHandler


class ExampleEndpoint(BackendRequestHandler):
    alias = "example"

    def get(self):
        self.write({"message": "Hello, world!"})


def get_handler():
    return ExampleEndpoint
