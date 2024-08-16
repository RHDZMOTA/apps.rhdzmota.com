from rhdzmota.apps.demo_whitehouse_virus_heatmap.frontend import view
from rhdzmota.apps.demo_whitehouse_virus_heatmap.backend import HelloHandler


if __name__ == "__main__":
    HelloHandler.register()
    view()
