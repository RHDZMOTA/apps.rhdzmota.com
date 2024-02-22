import json

import streamlit as st


@st.cache_data
def get_pages_configs() -> dict:
    with open("./pages.json", "r") as file:
        content = file.read()
    return json.loads(content)


def view():
    st.markdown("# [RHDZMOTA](https://rhdzmota.com) App Bundle")

    pages_config = get_pages_configs()
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
    view()
