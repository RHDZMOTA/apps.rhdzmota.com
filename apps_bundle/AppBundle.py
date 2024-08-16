import json
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import PageView


class Main(PageView):

    def get_page_icon_kwargs(self) -> dict:
        if not self.favicon_path:
            return {}
        return {"page_icon": self.favicon_path}

    @staticmethod
    @st.cache_data
    def get_pages_configs(path: Optional[str] = None) -> dict:
        filepath = path or "./pages.json"
        with open(filepath, "r") as file:
            content = file.read()
        return json.loads(content)
    
    @staticmethod
    def get_main_configs(path: Optional[str] = None) -> dict:
        filepath = path or "./config.json"
        with open(filepath, "r") as file:
            content = file.read()
        return json.loads(content)
    
    def view(self):
        st.markdown("# [RHDZMOTA](https://rhdzmota.com) App Bundle")
    
        pages_config = self.get_pages_configs()
        st.table(
            data=[
                {
                    "Page": page_config.get("page_alias", page_key),
                    "Description": page_config.get("page_description", ""),
                    "Streamlit Frontend Enabled": page_config.get("callable_frontend") is not None,
                    "Tornado API Backend Enabled": page_config.get("callable_backend") is not None,
                }
                for page_key, page_config in pages_config.items()
            ],
        )

if __name__ == "__main__":
    with Main(favicon_path="./favicon.png", **Main.get_main_configs()) as main:
        main.view()
