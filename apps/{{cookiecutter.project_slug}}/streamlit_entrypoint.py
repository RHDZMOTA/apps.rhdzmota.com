from rhdzmota.apps.{{cookiecutter.project_slug}}.frontend import view
from rhdzmota.apps.{{cookiecutter.project_slug}}.backend import HelloHandler


if __name__ == "__main__":
    HelloHandler.register()
    view()
