# apps.rhdzmota.com

Opinionated design patterns to manage streamlit application bundles and hack backend endpoints into the already existing tornado server.

----

This repo contains my personal streamlit applications and an opinionated approach on how to mange a collection of streamling apps. In essense, each streamlit is a single-page implementation that can be exceuted in an standalone environment, but can also be bundle together with other apps (multi-page streamlit app). Morevoer, we hack our way into the tornado server to expose prive api within our applications.

## Setup

### Python environment (optional)

Define the python version to use in the project:

```commandline
$ pyenv local 3.10.12
```

Create and activate the virtual environment:

```commandline
$ pyenv exec python -m venv venv
```
* Mac/Linux: `source venv/bin/activate`
* Windows: `source venv/Scripts/activate`

### Install python requriements

Project requirements:

```commandline
$ python -m pip install -r requirements.txt
```

Development requirements:

```commandline
$ python -m pip instll -r requirements-develop.txt
```

