import os

with open(os.path.join(os.path.dirname(__file__), "hello_world_version"), "r") as file:
    version = file.readline().strip()
