import enum
import textwrap
from typing import Optional

import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import PageView
from rhdzmota.ext.streamlit_webapps.backend import BackendRequestHandler
from rhdzmota.apps.hello_world.utils import Salutation


class FrontendView(PageView):

    def view(self):
        st.markdown("# Example App: hello-world")
    
        st.markdown(
            textwrap.dedent(
                """
                Example hello-world application designed by 
                [Rodrigo H. Mota](https://rhdzmota.com).
                """
            )
        )
    
        with st.form("form-hello-world"):
            recipient = st.text_input(label="Recipient", value="World")
            salutation = st.selectbox(
                label="Salutation",
                options=[
                    salutation
                    for salutation in Salutation
                ],
                format_func=lambda salutation: salutation.name.title()
            )
            submitted = st.form_submit_button("Submit")
        if not submitted:
            return
        st.markdown(f"> {salutation.value}, {recipient}!")
