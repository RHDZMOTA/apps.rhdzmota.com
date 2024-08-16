import textwrap

import streamlit as st

from rhdzmota.utils.misc import get_random_string
from rhdzmota.ext.streamlit_webapps.page_view import PageView


class FrontendView(PageView):
    

    def view(self):

        st.markdown("# Password Generator")
        query_params = st.query_params.to_dict()
        max_length = int(query_params.get("max_length") or 20)
        min_length = int(query_params.get("min_length") or 4)
        with st.form("pwd-gen-form"):
            length = st.slider(
                "PWD Length",
                min_value=min_length,
                max_value=max_length,
                value=10,
                step=1,
                )
            include_digits = st.toggle("Include Numbers")
            include_special_characters = st.toggle("Include Special Chars")
            case_sensitive = st.checkbox("Case Sensitive")
            submitted = st.form_submit_button("Generate")

        if not submitted:
            return

        pwd = get_random_string(
            length=length,
            include_digits=include_digits,
            include_special_characters=include_special_characters,
            case_sensitive=case_sensitive,
        )

        st.markdown(f"## Generated password: `{pwd}`")
        st.markdown(textwrap.dedent(
            f"""
            ```
            {pwd}
            ```
            """
        ))
