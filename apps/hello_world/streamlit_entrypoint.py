from rhdzmota.apps.hello_world.frontend import view
from rhdzmota.apps.hello_world.backend import HelloHandler


if __name__ == "__main__":
    HelloHandler.register()
    view()
