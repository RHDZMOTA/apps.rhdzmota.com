import textwrap
from typing import Any, Callable, Optional

import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import PageView
from rhdzmota.ext.streamlit_webapps.backend import BackendRequestHandler

from rhdzmota.apps.json_formatter.parser import JSONParser


class Remember:
    VAULT: dict[str, Callable[..., Any]] = {}

    def __init__(self, key: str, item_invoke_callable: Callable[..., Any]):
        self.VAULT[key] = item_invoke_callable

    @staticmethod
    @st.cache_data
    def get(key: str) -> Any:
        return Remember.VAULT[key]()

class FrontendView(PageView):
    def view(self):
        st.markdown("# Tool: JSON Parser")
    
        st.markdown(
            textwrap.dedent(
                """
                Simple JSON Parser tool designed by [Rodrigo H. Mota](https://rhdzmota.com) as an example streamlit application.
                """
            )
        )
    
        with st.form("json-parser-input-form"):
            json_string = st.text_area(label="JSON String")
            use_single_quotes = st.checkbox("Use Single Quotes")
            include_content_uuid = st.checkbox("Include Content UUID")
            include_yaml = st.checkbox("Include YAML equivalent")
            enable_cache_1h = st.checkbox("Cache 1h")
            flatten_output = st.selectbox(
                label="Flatten Config",
                options=[
                    "Disabled",
                    "Enabled without nested Lists",
                    "Enabled including nested Lists",
                ]
            )
            
            submitted = st.form_submit_button("Parse!")
    
        if not submitted:
            return
        elif not json_string:
            return st.warning("JSON String not detected!")
    
        parser = JSONParser(
            string=json_string,
            use_single_quotes=use_single_quotes
        )
        parser_uuid = parser.uuid
        json_output = Remember(
            key=parser_uuid,
            item_invoke_callable=parser.parse
        ).get(parser_uuid) if enable_cache_1h else parser.parse()
        #json_output = Remember(**{parser.uuid: parser.parse(fail=None)}).get(parser.uuid)
        
        if not json_output.ok:
            return st.warning("Error when parsing the provided JSON.")
    
        st.info("JSON String parsing success!")
        st.markdown("## Parsed JSON")
    
        # Display content uuid
        st.markdown(
            textwrap.dedent(
                f"""
                Content UUID: `{parser.uuid}`
                """
            )
        ) if include_content_uuid else None
    
        # Display parsed json
        st.json(json_output.payload)
        
        # Display flatten json if requested
        if "enable" in flatten_output.lower():
            st.markdown("### Flatten Representation")
            st.json(json_output.flatten(include_lists="without" not in flatten_output))
    
        if include_yaml:
            import yaml
    
            st.markdown("### YAML Representation")
            st.text(yaml.dump(json_output.payload))
