import os
import json
import textwrap
import datetime as dt
from typing import Optional
from dataclasses import dataclass

import fire


STREAMLIT_PAGE_TEMPLATE =  textwrap.dedent(
    """
    import streamlit as st

    {front_imports}
    {back_imports}

    
    # Start backend (if any)
    st.cache_resource({back_callable})(page_endpoint={page_endpoint})

    # Execute streamlit frontend code
    {front_callable}()
    """
)


@dataclass
class StreamlitPageTemplate:
    page_name: str
    page_endpoint: str
    page_alias: Optional[str] = None
    page_description: Optional[str] = None
    package_name: Optional[str] = None
    package_reference_frontend: Optional[str] = None
    package_reference_backend: Optional[str] = None
    callable_frontend: Optional[str] = None
    callable_backend: Optional[str] = None

    def dynamic_install(self):
        if not self.package_name:
            raise ValueError(
                "Cannot dynamically install package if pacakge_name is None"
            )
        path = os.getcwd()
        package_path = os.path.join(path, "apps", self.package_name)
        if not os.path.exists(package_path):
            raise ValueError(f"Package not found: {package_path}")
        return os.system(f"pip install -e {package_path}")

    def get_imports_frontend(self) -> tuple:
        if not self.package_reference_frontend:
            return "(lambda: st.title('Undefined'))", "import streamlit as st"
        return self.callable_frontend, textwrap.dedent(
            f"""
            from {self.package_reference_frontend} import {self.callable_frontend}
            """
        )

    def get_imports_backend(self) -> tuple:
        if not self.package_reference_backend: 
            return f"(lambda **kwargs: print('Backend not found for page: {self.page_name}'))", ""
        return self.callable_backend, textwrap.dedent(
            f"""
            from {self.package_reference_backend} import {self.callable_backend}
            """
        )

    @property
    def filename(self) -> str:
        return f"{self.page_name}.py"

    def save(self, path: str):
        content = self.get_page_content()
        with open(os.path.join(path, self.filename), "w") as file:
            file.write(content)

    def get_page_content(self) -> str:
        front_callable, front_imports = self.get_imports_frontend()
        back_callable, back_imports = self.get_imports_backend()
        return STREAMLIT_PAGE_TEMPLATE.format(
            page_endpoint=repr(self.page_endpoint),
            # Frontend components
            front_imports=front_imports,
            front_callable=front_callable,
            # Backend components
            back_imports=back_imports,
            back_callable=back_callable,
        )

class CLI:
    
    def __init__(
            self,
            apps_bundle_dirname: Optional[str] = None,
            apps_bundle_basepath: Optional[str] = None,
            disable_dynamic_install: bool = False,
    ):
        self.start = dt.datetime.utcnow()
        self.disable_dynamic_install = disable_dynamic_install
        self.apps_bundle_dirname = os.environ.get("APPS_BUNDLE_DIRNAME", default="apps_bundle")
        self.apps_bundle_basepath = os.environ.get("APPS_BUNDLE_BASEPATH", default=".")
        self.apps_bundle_config_filename = os.environ.get("APPS_BUNDLE_CONFIG_FILENAME", default="pages.json")
    
    @property
    def apps_bundle_path(self) -> str:
        path = os.path.join(self.apps_bundle_basepath, self.apps_bundle_dirname)
        if not os.path.exists(path):
            raise ValueError(f"Bundle Path does not exists: {path}")
        return path

    @property
    def apps_bundle_config_path(self) -> str:
        config_path = os.path.join(self.apps_bundle_path, self.apps_bundle_config_filename)
        if not os.path.exists(config_path):
            raise ValueErrorR(f"Bundle Config does not exists: {config_path}")
        return config_path

    @property
    def apps_bundle_config(self) -> dict:
        with open(self.apps_bundle_config_path, "r") as file:
            content = file.read()
        return json.loads(content)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def page_config(self, key: str) -> dict:
        config = self.apps_bundle_config.get(key, {})
        if not config:
            print("Config not found, using empty payload for page-key {key}")
        return config

    def template(self, page_key: str) -> StreamlitPageTemplate:
        config = self.page_config(key=page_key)
        page_name = config.get("page_alias", page_key)
        page_template = StreamlitPageTemplate(page_name=page_name, page_endpoint=page_key, **config)
        if not self.disable_dynamic_install:
            page_template.dynamic_install()
        return page_template

    def save(self, page_key: str, overwrite_output_path: Optional[str] = None) -> bool:
        print(f"Working on build for page key: {page_key}")
        path = os.path.join(self.apps_bundle_path, "pages")
        streamlit_template = self.template(page_key=page_key)
        streamlit_template.save(path=path)
        page_filepath = os.path.join(path, streamlit_template.page_name) + ".py"
        return os.path.exists(page_filepath)


    def build_bundle(self) -> dict:
        return {
            page_key: self.save(page_key=page_key)
            for page_key in self.apps_bundle_config.keys()
        }




if __name__ == "__main__":
    with CLI() as cli:
        fire.Fire(cli)
