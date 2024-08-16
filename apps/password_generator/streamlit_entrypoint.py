from rhdzmota.apps.password_generator.frontend import view
from rhdzmota.apps.password_generator.backend import HelloHandler


if __name__ == "__main__":
    HelloHandler.register()
    view()
